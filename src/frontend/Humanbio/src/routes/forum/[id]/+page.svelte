<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { auth } from "$lib/stores/auth";
    import { API_URL } from "$lib/constants";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { fade, fly, slide } from "svelte/transition";
    import { goto } from "$app/navigation";

    let post = $state(null);
    let loading = $state(true);
    let error = $state("");

    // Comment state
    let newComment = $state("");
    let replyContent = $state("");
    let replyingTo = $state(null); // ID of comment being replied to
    let posting = $state(false);
    let activeInput = $state(null);
    let expandedThreads = $state(new Set());

    let postId = $page.params.id;

    onMount(async () => {
        await fetchPost();
    });

    async function fetchPost() {
        try {
            const res = await fetch(`${API_URL}/api/forum/posts/${postId}`, {
                headers: $auth.isAuthenticated
                    ? {
                          Authorization: `Bearer ${$auth.token}`,
                      }
                    : {},
            });
            if (res.ok) {
                post = await res.json();
            } else {
                error = "Không tìm thấy bài viết";
            }
        } catch (e) {
            error = "Đã xảy ra lỗi kết nối";
        } finally {
            loading = false;
        }
    }

    async function handleReaction(targetType, id) {
        if (!$auth.isAuthenticated) {
            goto(`/login?redirect=/forum/${postId}`);
            return;
        }

        const endpoint =
            targetType === "post"
                ? `${API_URL}/api/forum/posts/${id}/react`
                : `${API_URL}/api/forum/comments/${id}/react`;

        try {
            const res = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({ type: "like" }),
            });

            if (res.ok) {
                // Optimistic update would be better, but re-fetching is safer for now
                await fetchPost();
            }
        } catch (e) {
            console.error("Reaction failed");
        }
    }

    async function postComment(parentId = null) {
        const content = parentId ? replyContent : newComment;
        if (!content.trim() || posting || !$auth.isAuthenticated) return;

        posting = true;
        try {
            const res = await fetch(
                `${API_URL}/api/forum/posts/${postId}/comments`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${$auth.token}`,
                    },
                    body: JSON.stringify({
                        content: content,
                        parent_id: parentId,
                    }),
                },
            );

            if (res.ok) {
                if (parentId) {
                    replyContent = "";
                    replyingTo = null;
                } else {
                    newComment = "";
                }
                await fetchPost(); // Refresh to show new comment/structure
            }
        } catch (e) {
            console.error("Failed to post comment");
        } finally {
            posting = false;
            activeInput = null;
        }
    }

    function toggleExpand(id) {
        if (expandedThreads.has(id)) {
            expandedThreads.delete(id);
        } else {
            expandedThreads.add(id);
        }
        expandedThreads = new Set(expandedThreads);
    }

    function formatDate(isoString) {
        return new Date(isoString).toLocaleDateString("vi-VN", {
            day: "numeric",
            month: "long",
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    function renderMarkdown(text) {
        if (!text) return "";
        let html = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\n/g, "<br/>");

        // Images: ![alt](url)
        html = html.replace(
            /!\[(.*?)\]\((.*?)\)/g,
            '<img src="$2" alt="$1" class="rounded-xl my-4 max-h-[500px] w-auto shadow-lg border border-fd-border/50" />',
        );

        // Links: [text](url)
        html = html.replace(
            /\[(.*?)\]\((.*?)\)/g,
            '<a href="$2" target="_blank" class="text-fd-primary hover:underline font-bold">$1</a>',
        );

        // Bold: **text**
        html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        // Italic: *text*
        html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");

        return html;
    }
</script>

<div class="max-w-4xl mx-auto px-6 py-10">
    <button
        onclick={() => goto("/forum")}
        class="text-fd-muted hover:text-fd-foreground font-bold text-xs uppercase tracking-wider mb-8 flex items-center gap-2 transition-colors"
    >
        <i class="bx bx-arrow-back text-lg"></i>
        Quay lại diễn đàn
    </button>

    {#if loading}
        <div class="flex justify-center py-20">
            <i class="bx bx-loader-alt animate-spin text-3xl text-fd-primary"
            ></i>
        </div>
    {:else if error}
        <div
            class="text-center py-20 bg-red-500/5 rounded-2xl border border-red-500/10"
        >
            <p class="text-red-500 font-bold">{error}</p>
        </div>
    {:else if post}
        <div class="space-y-12" in:fade>
            <!-- Post Content -->
            <div
                class="fd-card !p-8 md:!p-10 !rounded-[2.5rem] shadow-2xl relative overflow-hidden bg-white/90"
            >
                <!-- Decorative Glow -->
                <div
                    class="absolute -top-32 -right-32 w-96 h-96 bg-fd-primary/5 rounded-full blur-[100px] pointer-events-none"
                ></div>

                <div
                    class="flex items-start justify-between gap-4 mb-8 pb-8 border-b border-fd-border/50 relative z-10"
                >
                    <div class="flex items-center gap-4">
                        <Avatar
                            seed={post.author.avatar_seed ||
                                post.author.username}
                            size={64}
                            class="rounded-2xl shadow-lg ring-4 ring-white"
                        />
                        <div>
                            <span
                                class="inline-block px-3 py-1 bg-fd-secondary rounded-full text-[10px] font-black uppercase tracking-widest text-fd-muted mb-2"
                            >
                                {post.topic || "Thảo luận chung"}
                            </span>
                            <h1
                                class="text-2xl md:text-4xl font-[900] tracking-tighter text-fd-foreground leading-[1.1]"
                            >
                                {post.title}
                            </h1>
                            <div
                                class="flex items-center gap-3 text-xs font-bold text-fd-muted mt-2"
                            >
                                <span class="text-fd-primary"
                                    >{post.author.username}</span
                                >
                                <span>•</span>
                                <span>{formatDate(post.created_at)}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    class="prose prose-lg prose-slate max-w-none text-fd-foreground/80 font-medium leading-loose relative z-10 whitespace-pre-wrap"
                >
                    {@html renderMarkdown(post.content)}
                </div>

                <!-- Post Actions -->
                <div
                    class="flex items-center gap-4 mt-8 pt-8 border-t border-fd-border/50"
                >
                    <button
                        onclick={() => handleReaction("post", post.id)}
                        class="flex items-center gap-2 px-4 py-2 rounded-xl transition-all font-bold text-sm {post.user_reaction ===
                        'like'
                            ? 'bg-red-500/10 text-red-500'
                            : 'bg-fd-secondary hover:bg-fd-secondary/80 text-fd-muted'}"
                    >
                        <i
                            class="bx {post.user_reaction === 'like'
                                ? 'bxs-heart'
                                : 'bx-heart'} text-xl"
                        ></i>
                        <span>{post.reaction_count || 0}</span>
                    </button>
                    <span
                        class="text-sm font-bold text-fd-muted flex items-center gap-2"
                    >
                        <i class="bx bx-message-rounded-dots text-xl"></i>
                        {post.comments.length} thảo luận
                    </span>
                </div>
            </div>

            <!-- Comments Section (Theory Style) -->
            <div class="max-w-[720px] mx-auto">
                <div class="flex items-center gap-4 mb-10 overflow-hidden">
                    <div
                        class="flex items-center gap-2 px-3 py-1 bg-fd-primary/10 rounded-full border border-fd-primary/20"
                    >
                        <div
                            class="w-1.5 h-1.5 bg-fd-primary rounded-full animate-pulse"
                        ></div>
                        <span
                            class="text-[11px] font-black uppercase tracking-[0.1em] text-fd-primary"
                        >
                            Luồng thảo luận
                        </span>
                    </div>
                    <div
                        class="h-px flex-1 bg-gradient-to-r from-fd-primary/30 to-transparent"
                    ></div>
                </div>

                <!-- Main Comment Input -->
                {#if $auth.isAuthenticated}
                    <div
                        class="group relative mb-16 transition-all duration-500 {activeInput ===
                        'main'
                            ? 'scale-[1.01]'
                            : ''}"
                    >
                        <div class="flex gap-5">
                            <div class="relative">
                                <Avatar
                                    seed={$auth.user?.username}
                                    size={38}
                                    class="rounded-full shadow-sm"
                                />
                            </div>
                            <div class="flex-1 space-y-4">
                                <div
                                    class="relative rounded-2xl p-4 transition-all duration-500 {activeInput ===
                                    'main'
                                        ? 'bg-fd-primary/[0.03]'
                                        : 'bg-transparent'}"
                                >
                                    <textarea
                                        bind:value={newComment}
                                        onfocus={() => (activeInput = "main")}
                                        onblur={() =>
                                            !newComment && (activeInput = null)}
                                        placeholder="Chia sẻ ý kiến sinh học của bạn..."
                                        class="w-full bg-transparent border-none text-fd-foreground placeholder:text-fd-muted/40 focus:ring-0 resize-none min-h-[50px] text-[15px] p-0 font-medium transition-all outline-none"
                                    ></textarea>

                                    <!-- Focus Indicator -->
                                    <div
                                        class="absolute bottom-0 left-1/2 -translate-x-1/2 h-[2px] bg-fd-primary transition-all duration-700 ease-out {activeInput ===
                                        'main'
                                            ? 'w-[80%] opacity-100 shadow-[0_0_15px_var(--primary-glow)]'
                                            : 'w-0 opacity-0'}"
                                    ></div>

                                    {#if activeInput === "main"}
                                        <div
                                            transition:slide
                                            class="flex items-center justify-between border-t border-fd-border/10 mt-4 pt-3"
                                        >
                                            <div class="flex gap-2">
                                                <span
                                                    class="text-[10px] font-bold text-fd-muted flex items-center gap-1"
                                                >
                                                    <i class="bx bx-info-circle"
                                                    ></i> Hỗ trợ Markdown & Ảnh
                                                </span>
                                            </div>
                                            <button
                                                onclick={() => postComment()}
                                                disabled={!newComment.trim() ||
                                                    posting}
                                                class="fd-btn-primary !py-2 !px-6 !text-[10px] !rounded-xl !font-black !uppercase !tracking-widest shadow-[0_10px_20px_-5px_var(--primary-glow)]"
                                            >
                                                {#if posting}
                                                    <i
                                                        class="bx bx-loader-alt animate-spin mr-2"
                                                    ></i> Đang gửi...
                                                {:else}
                                                    Gửi ý kiến
                                                {/if}
                                            </button>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    </div>
                {:else}
                    <div
                        class="mb-16 p-6 rounded-3xl bg-fd-primary/5 border border-dashed border-fd-primary/20 text-center"
                    >
                        <a
                            href="/login?redirect=/forum/{postId}"
                            class="text-[13px] font-bold text-fd-primary hover:underline"
                        >
                            Đăng nhập để tham gia thảo luận
                        </a>
                    </div>
                {/if}

                <!-- Comment List -->
                <div class="space-y-4">
                    {#each post.comments as comment (comment.id)}
                        {@render threadNode(comment)}
                    {/each}

                    {#if post.comments.length === 0}
                        <div class="text-center py-20 opacity-30">
                            <i class="bx bx-dna text-5xl mb-4 text-fd-muted"
                            ></i>
                            <p class="text-sm font-bold italic">
                                Chưa có hoạt động nơ-ron nào ở đây.
                            </p>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    {/if}
</div>

{#snippet threadNode(comment, depth = 0)}
    <div class="relative group" in:fade>
        <div class="flex gap-4 pt-4">
            <!-- Thread Line -->
            <div class="flex flex-col items-center relative">
                <div class="relative">
                    <Avatar
                        seed={comment.author.avatar_seed}
                        size={depth > 0 ? 30 : 36}
                        class="rounded-full z-10 shadow-sm"
                    />
                </div>
                {#if (comment.replies && comment.replies.length > 0) || replyingTo === comment.id}
                    <div
                        class="absolute top-10 bottom-0 w-[2px] bg-gradient-to-b from-fd-primary/40 to-fd-primary/5"
                    ></div>
                {/if}
            </div>

            <div
                class="flex-1 min-w-0 pb-8 {depth === 0
                    ? 'border-b border-fd-border/10'
                    : ''}"
            >
                <div class="flex items-center justify-between mb-1.5">
                    <div class="flex items-center gap-2">
                        <span
                            class="text-[14px] font-black text-fd-foreground hover:text-fd-primary cursor-pointer transition-colors tracking-tight"
                        >
                            {comment.author.username}
                        </span>
                        {#if comment.author.username === post.author.username}
                            <span
                                class="px-1.5 py-0.5 rounded-md bg-fd-primary/5 text-[9px] font-black text-fd-primary uppercase tracking-tighter"
                                >Tác giả</span
                            >
                        {/if}
                    </div>
                    <span
                        class="text-[10px] font-bold text-fd-muted opacity-50 uppercase tracking-tighter"
                    >
                        {formatDate(comment.created_at)}
                    </span>
                </div>

                <div
                    class="text-[15px] text-fd-muted-foreground leading-relaxed break-words font-medium"
                >
                    {@html renderMarkdown(comment.content)}
                </div>

                <div class="flex items-center gap-6 mt-4">
                    <button
                        onclick={() => handleReaction("comment", comment.id)}
                        class="text-[10px] font-black uppercase tracking-[0.15em] transition-all flex items-center gap-2 group/btn {comment.user_reaction ===
                        'like'
                            ? 'text-red-500'
                            : 'text-fd-muted hover:text-red-500'}"
                    >
                        <i
                            class="bx {comment.user_reaction === 'like'
                                ? 'bxs-heart'
                                : 'bx-heart'} text-sm"
                        ></i>
                        {comment.reaction_count || 0}
                    </button>

                    {#if $auth.isAuthenticated}
                        <button
                            onclick={() =>
                                (replyingTo =
                                    replyingTo === comment.id
                                        ? null
                                        : comment.id)}
                            class="text-[10px] font-black uppercase tracking-[0.15em] text-fd-muted hover:text-fd-primary transition-all flex items-center gap-2 group/btn"
                        >
                            <div
                                class="w-6 h-6 rounded-full bg-fd-accent/50 flex items-center justify-center group-hover/btn:bg-fd-primary group-hover/btn:text-white transition-all"
                            >
                                <i
                                    class="bx {replyingTo === comment.id
                                        ? 'bx-x'
                                        : 'bx-reply'} text-sm"
                                ></i>
                            </div>
                            {replyingTo === comment.id ? "Hủy" : "Trả lời"}
                        </button>
                    {/if}
                </div>

                <!-- Glow Inline Reply -->
                {#if replyingTo === comment.id}
                    <div transition:slide class="mt-5 relative group/reply">
                        <div
                            class="absolute -left-6 top-1/2 -translate-y-1/2 w-4 h-[px] bg-fd-primary/30"
                        ></div>
                        <div
                            class="bg-fd-primary/[0.02] p-4 rounded-2xl transition-all duration-300"
                        >
                            <textarea
                                bind:value={replyContent}
                                onfocus={() => (activeInput = comment.id)}
                                onblur={() =>
                                    !replyContent && (activeInput = null)}
                                placeholder="Phản hồi tới {comment.author
                                    .username}..."
                                class="w-full bg-transparent border-none text-fd-foreground placeholder:text-fd-muted/50 focus:ring-0 resize-none min-h-[45px] text-[14px] p-0 font-medium outline-none"
                            ></textarea>

                            <div
                                class="h-[1.5px] bg-fd-primary transition-all duration-500 ease-out {activeInput ===
                                comment.id
                                    ? 'w-full opacity-100'
                                    : 'w-0 opacity-0'}"
                            ></div>

                            <div
                                class="flex justify-end pt-3 border-t border-fd-border/10 mt-3"
                            >
                                <button
                                    onclick={() => postComment(comment.id)}
                                    disabled={!replyContent.trim() || posting}
                                    class="text-[10px] font-black uppercase tracking-widest text-fd-primary hover:opacity-70 disabled:opacity-30 flex items-center gap-2"
                                >
                                    {#if posting}
                                        <i class="bx bx-loader-alt animate-spin"
                                        ></i>
                                    {/if}
                                    Gửi phản hồi
                                </button>
                            </div>
                        </div>
                    </div>
                {/if}

                <!-- Nested Replies -->
                {#if comment.replies && comment.replies.length > 0}
                    <div class="mt-4">
                        {#if !expandedThreads.has(comment.id)}
                            <button
                                onclick={() => toggleExpand(comment.id)}
                                class="flex items-center gap-2 group/reveal transition-all"
                            >
                                <div
                                    class="flex -space-x-1.5 transition-all group-hover/reveal:mr-2"
                                >
                                    {#each comment.replies.slice(0, 3) as reply}
                                        <Avatar
                                            seed={reply.author.avatar_seed}
                                            size={18}
                                            class="rounded-full ring-2 ring-fd-background border border-fd-border/30"
                                        />
                                    {/each}
                                </div>
                                <span
                                    class="text-[10px] font-black uppercase tracking-widest text-fd-primary hover:text-fd-primary/70 flex items-center gap-1.5"
                                >
                                    Xem {comment.replies.length} câu trả lời
                                    <i
                                        class="bx bx-chevron-down text-sm transition-transform group-hover/reveal:translate-y-0.5"
                                    ></i>
                                </span>
                            </button>
                        {:else}
                            <div
                                class="space-y-2 border-l-2 border-fd-border/10"
                            >
                                <button
                                    onclick={() => toggleExpand(comment.id)}
                                    class="ml-4 mb-2 text-[10px] font-black uppercase tracking-widest text-fd-muted hover:text-fd-primary transition-colors flex items-center gap-1"
                                >
                                    Thu gọn <i class="bx bx-chevron-up"></i>
                                </button>
                                {#each comment.replies as reply (reply.id)}
                                    <div class="pl-4">
                                        {@render threadNode(reply, depth + 1)}
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/snippet}

<style>
    textarea {
        transition: all 0.3s ease;
    }
</style>
