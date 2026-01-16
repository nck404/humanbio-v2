<script>
    import { fade } from "svelte/transition";
</script>

<div class="max-w-4xl mx-auto py-16 px-6">
    <div class="mb-12 text-center" in:fade>
        <h1
            class="text-4xl font-extrabold text-fd-foreground tracking-tight mb-4"
        >
            Quy tắc cộng đồng
        </h1>
        <p class="text-fd-muted font-medium text-lg">
            Để xây dựng một môi trường học tập lành mạnh và tôn trọng lẫn nhau.
        </p>
    </div>

    <div class="space-y-8" in:fade={{ delay: 100 }}>
        <!-- General Rules -->
        <div class="fd-card p-8">
            <h2
                class="text-xl font-black uppercase tracking-widest text-fd-primary flex items-center gap-3 mb-6"
            >
                <i class="bx bx-shield-quarter text-2xl"></i>
                Quy tắc chung
            </h2>
            <div class="space-y-4">
                <div class="flex gap-4">
                    <span class="text-2xl font-black text-fd-primary/20"
                        >01</span
                    >
                    <div>
                        <h3 class="text-lg font-bold text-fd-foreground">
                            Tôn trọng lẫn nhau
                        </h3>
                        <p class="text-fd-muted leading-relaxed">
                            Không sử dụng ngôn từ xúc phạm, quấy rối, phân biệt
                            chủng tộc, tôn giáo, giới tính hoặc bất kỳ hình thức
                            phân biệt đối xử nào khác. Hãy đối xử với người khác
                            như cách bạn muốn được đối xử.
                        </p>
                    </div>
                </div>

                <div class="flex gap-4">
                    <span class="text-2xl font-black text-fd-primary/20"
                        >02</span
                    >
                    <div>
                        <h3 class="text-lg font-bold text-fd-foreground">
                            Không nội dung độc hại
                        </h3>
                        <p class="text-fd-muted leading-relaxed">
                            Cấm tuyệt đối việc chia sẻ nội dung khiêu dâm, bạo
                            lực, lừa đảo, hoặc các nội dung vi phạm pháp luật
                            Việt Nam.
                        </p>
                    </div>
                </div>

                <div class="flex gap-4">
                    <span class="text-2xl font-black text-fd-primary/20"
                        >03</span
                    >
                    <div>
                        <h3 class="text-lg font-bold text-fd-foreground">
                            Không Spam
                        </h3>
                        <p class="text-fd-muted leading-relaxed">
                            Không đăng tải các nội dung rác, quảng cáo không
                            liên quan, hoặc lặp đi lặp lại cùng một nội dung
                            nhiều lần.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Academic Integrity -->
        <div class="fd-card p-8 bg-fd-accent/10 border-fd-primary/20">
            <h2
                class="text-xl font-black uppercase tracking-widest text-fd-foreground flex items-center gap-3 mb-6"
            >
                <i class="bx bx-book-open text-2xl"></i>
                Liêm chính học thuật
            </h2>
            <div class="space-y-4">
                <div class="flex gap-4">
                    <span class="text-2xl font-black text-fd-foreground/20"
                        >04</span
                    >
                    <div>
                        <h3 class="text-lg font-bold text-fd-foreground">
                            Không gian lận
                        </h3>
                        <p class="text-fd-muted leading-relaxed">
                            Các bài kiểm tra nên phản ánh đúng năng lực của bạn.
                            Không chia sẻ đáp án bài kiểm tra, hoặc hỏi đáp án
                            trong các bài kiểm tra đánh giá năng lực.
                        </p>
                    </div>
                </div>
                <div class="flex gap-4">
                    <span class="text-2xl font-black text-fd-foreground/20"
                        >05</span
                    >
                    <div>
                        <h3 class="text-lg font-bold text-fd-foreground">
                            Chia sẻ kiến thức
                        </h3>
                        <p class="text-fd-muted leading-relaxed">
                            Khuyến khích việc chia sẻ kiến thức, tài liệu học
                            tập hữu ích và giúp đỡ nhau cùng tiến bộ. Hãy trích
                            dẫn nguồn nếu bạn sử dụng tài liệu của người khác.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Enforcement -->
        <div class="fd-card p-8 bg-red-500/5 border-red-500/10">
            <h2
                class="text-xl font-black uppercase tracking-widest text-red-500 flex items-center gap-3 mb-6"
            >
                <i class="bx bx-error-circle text-2xl"></i>
                Xử lý vi phạm
            </h2>
            <div class="text-fd-muted leading-relaxed space-y-2">
                <p>
                    <span class="font-bold text-fd-foreground"
                        >Vi phạm lần 1:</span
                    > Nhắc nhở và xóa nội dung vi phạm. Thông báo sẽ được gửi qua
                    hộp thư.
                </p>
                <p>
                    <span class="font-bold text-fd-foreground"
                        >Vi phạm lần 2:</span
                    > Khóa tài khoản tạm thời (3-7 ngày).
                </p>
                <p>
                    <span class="font-bold text-fd-foreground"
                        >Vi phạm nghiêm trọng:</span
                    > Khóa tài khoản vĩnh viễn ngay lập tức.
                </p>
                <p class="text-xs italic mt-4 opacity-70">
                    * Ban quản trị có quyền quyết định cuối cùng trong mọi
                    trường hợp.
                </p>
            </div>
        </div>
    </div>
</div>

<style>
    :global(.fd-card) {
        background: var(--fd-card);
        border: 1px solid var(--fd-border);
        border-radius: 1.5rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
</style>
