<script>
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth";
    import { API_URL } from "$lib/constants";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { fade, fly } from "svelte/transition";

    let posts = $state([]);
    let loading = $state(true);
    let error = $state("");

    onMount(async () => {
        await fetchPosts();
    });

    async function fetchPosts() {
        try {
            const res = await fetch(`${API_URL}/api/forum/posts`);
            if (res.ok) {
                posts = await res.json();
            } else {
                error = "Không thể tải danh sách bài viết";
            }
        } catch (e) {
            error = "Đã xảy ra lỗi kết nối";
        } finally {
            loading = false;
        }
    }

    function formatDate(isoString) {
        return new Date(isoString).toLocaleDateString("vi-VN", {
            day: "numeric",
            month: "long",
            hour: "2-digit",
            minute: "2-digit",
        });
    }
</script>

<div class="max-w-5xl mx-auto px-6 py-10">
    <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10"
    >
        <div in:fly={{ y: 20, duration: 600 }}>
            <h1
                class="text-3xl font-[900] tracking-tighter text-fd-foreground mb-2"
            >
                Diễn đàn thảo luận
                <span class="text-fd-primary">.</span>
            </h1>
            <p class="text-fd-muted font-medium text-sm max-w-lg">
                Không gian trao đổi kiến thức, giải đáp thắc mắc và chia sẻ niềm
                đam mê sinh học.
            </p>
        </div>

        <a
            href="/forum/new"
            class="fd-btn-primary !rounded-xl !px-6 !py-3 shadow-lg shadow-fd-primary/20 hover:translate-y-[-2px] transition-transform"
            in:fly={{ y: 20, duration: 800 }}
        >
            <i class="bx bx-plus-circle mr-2 text-lg"></i>
            Tạo bài viết mới
        </a>
    </div>

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
            <button
                onclick={fetchPosts}
                class="mt-4 text-xs font-black uppercase tracking-widest hover:underline text-red-500"
                >Thử lại</button
            >
        </div>
    {:else if posts.length === 0}
        <div
            class="text-center py-20 bg-fd-secondary/30 rounded-3xl border-2 border-dashed border-fd-border/50"
        >
            <div
                class="w-16 h-16 bg-fd-secondary rounded-full flex items-center justify-center mx-auto mb-4"
            >
                <i class="bx bx-message-square-dots text-2xl text-fd-muted"></i>
            </div>
            <h3 class="text-lg font-bold text-fd-foreground mb-2">
                Chưa có bài viết nào
            </h3>
            <p class="text-fd-muted text-sm mb-6">
                Hãy là người đầu tiên bắt đầu cuộc thảo luận!
            </p>
            <a
                href="/forum/new"
                class="text-fd-primary font-bold hover:underline text-sm"
                >Viết bài ngay</a
            >
        </div>
    {:else}
        <div class="grid gap-4">
            {#each posts as post, i}
                <a
                    href="/forum/{post.id}"
                    class="group relative fd-card !p-6 !rounded-2xl hover:bg-fd-secondary/30 transition-all hover:scale-[1.01] hover:shadow-xl border border-fd-border/50 hover:border-fd-primary/20"
                    in:fly={{ y: 20, delay: i * 50 }}
                >
                    <div class="flex items-start gap-4">
                        <Avatar
                            seed={post.author.avatar_seed ||
                                post.author.username}
                            size={42}
                            class="rounded-xl shadow-sm"
                        />
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center gap-2 mb-1.5">
                                <span
                                    class="text-xs font-black text-fd-primary bg-fd-primary/10 px-2 py-0.5 rounded-md uppercase tracking-wider"
                                    >{post.topic || "Thảo luận"}</span
                                >
                                <span
                                    class="text-[11px] font-bold text-fd-muted"
                                    >•</span
                                >
                                <span
                                    class="text-[11px] font-bold text-fd-muted"
                                    >{post.author.username}</span
                                >
                                <span
                                    class="text-[11px] font-bold text-fd-muted"
                                    >•</span
                                >
                                <span
                                    class="text-[11px] font-medium text-fd-muted"
                                    >{formatDate(post.created_at)}</span
                                >
                            </div>
                            <h3
                                class="text-lg font-bold text-fd-foreground mb-2 group-hover:text-fd-primary transition-colors line-clamp-1"
                            >
                                {post.title}
                            </h3>
                            <p
                                class="text-sm text-fd-muted line-clamp-2 mb-4 font-medium opacity-80"
                            >
                                {post.content}
                            </p>

                            <div
                                class="flex items-center gap-4 text-xs font-bold text-fd-muted"
                            >
                                <div
                                    class="flex items-center gap-1.5 group-hover:text-fd-primary transition-colors"
                                >
                                    <i
                                        class="bx bx-message-rounded-dots text-base"
                                    ></i>
                                    {post.comment_count} bình luận
                                </div>
                                <div class="flex items-center gap-1.5">
                                    <i class="bx bx-show text-base"></i>
                                    Xem chi tiết
                                </div>
                            </div>
                        </div>
                        <div
                            class="self-center opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 duration-300"
                        >
                            <i
                                class="bx bx-chevron-right text-2xl text-fd-muted"
                            ></i>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>
