<script>
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth";
    import { fade, fly, slide } from "svelte/transition";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { API_URL } from "$lib/constants";
    import { viewedUserId } from "$lib/stores/ui";

    let { slug } = $props();

    let comments = $state([]);
    let newComment = $state("");
    let replyContent = $state("");
    let replyingTo = $state(null);
    let loading = $state(true);
    let posting = $state(false);
    let activeInput = $state(null); // 'main' or comment ID
    let expandedThreads = $state(new Set());

    function toggleExpand(id) {
        if (expandedThreads.has(id)) {
            expandedThreads.delete(id);
        } else {
            expandedThreads.add(id);
        }
        // Force reactivity in Svelte 5 for Set
        expandedThreads = new Set(expandedThreads);
    }

    onMount(async () => {
        await fetchComments();
    });

    async function fetchComments() {
        loading = true;
        try {
            const res = await fetch(`${API_URL}/api/comments/${slug}`);
            if (res.ok) {
                comments = await res.json();
            }
        } catch (e) {
            console.error("Failed to fetch comments", e);
        } finally {
            loading = false;
        }
    }

    async function postComment(parentId = null) {
        const content = parentId ? replyContent : newComment;
        if (!content.trim() || posting || !$auth.isAuthenticated) return;

        posting = true;
        try {
            const res = await fetch(`${API_URL}/api/comments`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({
                    content: content,
                    slug: slug,
                    parent_id: parentId,
                }),
            });

            if (res.ok) {
                const data = await res.json();
                if (parentId) {
                    addReplyLocally(comments, parentId, data.comment);
                    replyContent = "";
                    replyingTo = null;
                } else {
                    comments = [data.comment, ...comments];
                    newComment = "";
                }
            }
        } catch (e) {
            console.error("Failed to post comment", e);
        } finally {
            posting = false;
            activeInput = null;
        }
    }

    function addReplyLocally(list, parentId, newReply) {
        for (let c of list) {
            if (c.id === parentId) {
                c.replies = [...(c.replies || []), newReply];
                return true;
            }
            if (c.replies && addReplyLocally(c.replies, parentId, newReply))
                return true;
        }
        return false;
    }

    function formatDate(dateStr) {
        const date = new Date(dateStr);
        const now = new Date();
        const diff = (now - date) / 1000;

        if (diff < 60) return "Just now";
        if (diff < 3600) return `${Math.floor(diff / 60)}m`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h`;
        return date.toLocaleDateString("vi-VN", {
            day: "2-digit",
            month: "2-digit",
        });
    }
</script>

<div
    class="mt-24 border-t border-fd-border/40 pt-12 mb-32 max-w-[720px] mx-auto"
>
    <div class="flex items-center gap-4 mb-10 overflow-hidden">
        <div
            class="flex items-center gap-2 px-3 py-1 bg-fd-primary/10 rounded-full border border-fd-primary/20"
        >
            <div
                class="w-1.5 h-1.5 bg-fd-primary rounded-full animate-pulse"
            ></div>
            <span
                class="text-[11px] font-black uppercase tracking-[0.1em] text-fd-primary"
                >Synaptic Thread</span
            >
        </div>
        <div
            class="h-px flex-1 bg-gradient-to-r from-fd-primary/30 to-transparent"
        ></div>
        <div class="flex -space-x-2">
            {#each comments.slice(0, 3) as c}
                <Avatar
                    seed={c.avatar_seed}
                    size={22}
                    class="rounded-full ring-2 ring-fd-background"
                />
            {/each}
        </div>
    </div>

    <!-- Main Post Box with Glow -->
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
                            onblur={() => !newComment && (activeInput = null)}
                            placeholder="Share your biological sequence..."
                            class="w-full bg-transparent border-none text-fd-foreground placeholder:text-fd-muted/40 focus:ring-0 resize-none min-h-[50px] text-[15px] p-0 font-medium transition-all outline-none"
                        ></textarea>

                        <!-- Interesting Focus Indicator: Expanding Center Line -->
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
                                        <i class="bx bx-info-circle"></i> Markdown
                                        enabled
                                    </span>
                                </div>
                                <button
                                    onclick={() => postComment()}
                                    disabled={!newComment.trim() || posting}
                                    class="fd-btn-primary !py-2 !px-6 !text-[10px] !rounded-xl !font-black !uppercase !tracking-widest shadow-[0_10px_20px_-5px_var(--primary-glow)]"
                                >
                                    {#if posting}
                                        <i
                                            class="bx bx-loader-alt animate-spin mr-2"
                                        ></i> Synching...
                                    {:else}
                                        Transmit Idea
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
            class="mb-16 p-6 rounded-3xl bg-fd-primary/5 border border-dashed border-fd-primary/20 text-center group hover:bg-fd-primary/10 transition-all"
        >
            <i class="bx bx-lock-alt text-2xl text-fd-primary mb-3 opacity-50"
            ></i>
            <p class="text-[13px] font-bold text-fd-muted leading-relaxed">
                Identity verification required to join the biological discourse.
            </p>
        </div>
    {/if}

    <!-- Thread List -->
    <div class="space-y-4 relative">
        {#if loading}
            <div class="flex flex-col items-center py-20 gap-4">
                <div
                    class="w-8 h-8 border-3 border-fd-primary/10 border-t-fd-primary rounded-full animate-spin"
                ></div>
                <span
                    class="text-[9px] font-black uppercase tracking-widest text-fd-primary opacity-40"
                    >Scanning DNA</span
                >
            </div>
        {:else if comments.length === 0}
            <div class="text-center py-20 opacity-30">
                <i class="bx bx-dna text-5xl mb-4 text-fd-muted"></i>
                <p class="text-sm font-bold italic">
                    No neural activity detected in this section.
                </p>
            </div>
        {:else}
            {#each comments as comment (comment.id)}
                {@render threadNode(comment)}
            {/each}
        {/if}
    </div>
</div>

{#snippet threadNode(comment, depth = 0)}
    <div class="relative group" in:fade>
        <div class="flex gap-4 pt-4">
            <!-- Thread Line with Dynamic Color -->
            <div class="flex flex-col items-center relative">
                <button
                    class="relative cursor-pointer transition-transform hover:scale-105 active:scale-95"
                    onclick={() => viewedUserId.set(comment.user_id)}
                    title="View Profile"
                >
                    <Avatar
                        url={comment.avatar_url}
                        seed={comment.avatar_seed}
                        size={depth > 0 ? 30 : 36}
                        class="rounded-full z-10 shadow-sm"
                    />
                </button>

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
                        <button
                            onclick={() => viewedUserId.set(comment.user_id)}
                            class="text-[14px] font-black text-fd-foreground hover:text-fd-primary cursor-pointer transition-colors tracking-tight text-left"
                        >
                            {comment.username}
                        </button>
                        {#if depth === 0}
                            <span
                                class="px-1.5 py-0.5 rounded-md bg-fd-primary/5 text-[9px] font-black text-fd-primary uppercase tracking-tighter"
                                >Contributor</span
                            >
                        {/if}
                    </div>
                    <span
                        class="text-[10px] font-bold text-fd-muted opacity-50 uppercase tracking-tighter"
                        >{formatDate(comment.created_at)}</span
                    >
                </div>

                <p
                    class="text-[15px] text-fd-muted-foreground leading-relaxed break-words font-medium"
                >
                    {comment.content}
                </p>

                <div class="flex items-center gap-6 mt-4">
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
                            {replyingTo === comment.id ? "Abort" : "Reply"}
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
                                placeholder="Genetic response for {comment.username}..."
                                class="w-full bg-transparent border-none text-fd-foreground placeholder:text-fd-muted/50 focus:ring-0 resize-none min-h-[45px] text-[14px] p-0 font-medium outline-none"
                            ></textarea>

                            <!-- Expanding Underline for Reply -->
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
                                    Send Signal
                                </button>
                            </div>
                        </div>
                    </div>
                {/if}

                <!-- Sub-thread Nested (Collapsible) -->
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
                                            seed={reply.avatar_seed}
                                            size={18}
                                            class="rounded-full ring-2 ring-fd-background border border-fd-border/30"
                                        />
                                    {/each}
                                </div>
                                <span
                                    class="text-[10px] font-black uppercase tracking-widest text-fd-primary hover:text-fd-primary/70 flex items-center gap-1.5"
                                >
                                    Show {comment.replies.length} replies
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
                                    Hide thread <i class="bx bx-chevron-up"></i>
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

    /* Animation for appearing messages */
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-fade-in {
        animation: fade-in-up 0.4s ease forwards;
    }
</style>
