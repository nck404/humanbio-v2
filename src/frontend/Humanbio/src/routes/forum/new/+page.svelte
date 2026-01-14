<script>
    import { auth } from "$lib/stores/auth";
    import { API_URL } from "$lib/constants";
    import { goto } from "$app/navigation";
    import { fade, fly } from "svelte/transition";

    let title = $state("");
    let content = $state("");
    let topic = $state("Thảo luận chung");
    let loading = $state(false);
    let error = $state("");

    $effect(() => {
        if (!$auth.isAuthenticated) {
            goto("/login?redirect=/forum/new");
        }
    });

    async function handleSubmit() {
        if (!title.trim() || !content.trim()) return;

        loading = true;
        error = "";

        try {
            const res = await fetch(`${API_URL}/api/forum/posts`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({ title, content, topic }),
            });

            if (res.ok) {
                const data = await res.json();
                goto(`/forum/${data.id}`);
            } else {
                const data = await res.json();
                error = data.msg || "Không thể tạo bài viết";
            }
        } catch (e) {
            error = "Đã xảy ra lỗi kết nối";
        } finally {
            loading = false;
        }
    }
</script>

<div class="max-w-3xl mx-auto px-6 py-10">
    <button
        onclick={() => goto("/forum")}
        class="text-fd-muted hover:text-fd-foreground font-bold text-xs uppercase tracking-wider mb-8 flex items-center gap-2 transition-colors"
    >
        <i class="bx bx-arrow-back text-lg"></i>
        Quay lại diễn đàn
    </button>

    <div class="fd-card !p-8 !rounded-[2rem] shadow-xl" in:fly={{ y: 20 }}>
        <h1 class="text-2xl font-[900] tracking-tight text-fd-foreground mb-1">
            Tạo thảo luận mới
        </h1>
        <p class="text-fd-muted text-sm font-medium mb-8">
            Đặt câu hỏi hoặc chia sẻ kiến thức với cộng đồng.
        </p>

        {#if error}
            <div
                class="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500 text-sm font-bold flex items-center gap-2"
            >
                <i class="bx bx-error-circle"></i>
                {error}
            </div>
        {/if}

        <form
            class="space-y-6"
            onsubmit={(e) => {
                e.preventDefault();
                handleSubmit();
            }}
        >
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="space-y-2 md:col-span-2">
                    <label for="title" class="fd-label ml-1"
                        >Tiêu đề bài viết</label
                    >
                    <input
                        id="title"
                        type="text"
                        bind:value={title}
                        required
                        placeholder="Ví dụ: Làm thế nào để phân biệt tế bào nhân sơ và nhân thực?"
                        class="fd-input w-full !text-lg !font-bold !py-4 !px-5 !rounded-xl"
                    />
                </div>
                <div class="space-y-2">
                    <label for="topic" class="fd-label ml-1">Chủ đề</label>
                    <div class="relative">
                        <select
                            id="topic"
                            bind:value={topic}
                            class="fd-input w-full !py-4 !px-5 !rounded-xl appearance-none font-bold"
                        >
                            <option>Thảo luận chung</option>
                            <option>Hỏi đáp bài tập</option>
                            <option>Chia sẻ tài liệu</option>
                            <option>Góp ý</option>
                        </select>
                        <i
                            class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-xl text-fd-muted pointer-events-none"
                        ></i>
                    </div>
                </div>
            </div>

            <div class="space-y-2">
                <label for="content" class="fd-label ml-1"
                    >Nội dung chi tiết</label
                >
                <textarea
                    id="content"
                    bind:value={content}
                    required
                    rows="8"
                    placeholder="Mô tả chi tiết vấn đề bạn đang quan tâm..."
                    class="fd-input w-full !py-4 !px-5 !rounded-xl resize-none leading-relaxed"
                ></textarea>
                <p
                    class="text-[10px] text-fd-muted font-bold pl-2 flex items-center gap-1"
                >
                    <i class="bx bx-info-circle"></i> Hỗ trợ chèn ảnh bằng Markdown:
                    ![mô tả](url_ảnh)
                </p>
            </div>

            <div class="pt-4 flex justify-end gap-4">
                <button
                    type="button"
                    onclick={() => goto("/forum")}
                    class="px-6 py-3 rounded-xl font-bold text-fd-muted hover:bg-fd-secondary/50 transition-colors"
                >
                    Hủy bỏ
                </button>
                <button
                    type="submit"
                    disabled={loading}
                    class="fd-btn-primary !rounded-xl !px-8 !py-3 shadow-lg shadow-fd-primary/20 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                    {#if loading}
                        <i class="bx bx-loader-alt animate-spin mr-2"></i>
                        Đang đăng...
                    {:else}
                        <i class="bx bx-send mr-2"></i>
                        Đăng bài viết
                    {/if}
                </button>
            </div>
        </form>
    </div>
</div>
