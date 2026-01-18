<script>
    import { fade } from "svelte/transition";
</script>

<div class="py-12 px-6">
    <div
        class="max-w-3xl mx-auto text-center mb-16"
        in:fade={{ duration: 800 }}
    >
        <div
            class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-fd-primary/10 border border-fd-primary/20 text-fd-primary text-[10px] font-bold uppercase tracking-widest mb-6"
        >
            <i class="bx bxs-book-open"></i>
            Kho lý thuyết
        </div>
        <h1
            class="text-5xl md:text-6xl font-black tracking-tight text-fd-foreground mb-6"
        >
            <span class="text-gradient">Sinh</span> Học
        </h1>
        <p class="text-lg text-fd-muted leading-relaxed max-w-2xl mx-auto">
            Khám phá sâu về sinh lý học, di truyền học và giải phẫu học. Những
            hiểu biết chọn lọc được phân loại để học tập hiệu quả
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <div
            class="fd-card group hover:border-fd-primary/50 transition-all duration-500"
        >
            <div
                class="w-12 h-12 bg-fd-primary/10 rounded-xl flex items-center justify-center text-fd-primary mb-6 group-hover:scale-110 transition-transform"
            >
                <i class="bx bx-subdirectory-right text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">Cấu trúc rõ ràng</h3>
            <p class="text-sm text-fd-muted font-medium">
                Sử dụng menu bên trái để chọn bài học và thông tin,
            </p>
        </div>

        <div
            class="fd-card group hover:border-fd-primary/50 transition-all duration-500"
        >
            <div
                class="w-12 h-12 bg-fd-primary/10 rounded-xl flex items-center justify-center text-fd-primary mb-6 group-hover:scale-110 transition-transform"
            >
                <i class="bx bx-search-alt text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">Search Anything</h3>
            <p class="text-sm text-fd-muted font-medium">
                Nhấn <kbd
                    class="px-1.5 py-0.5 bg-fd-accent border border-fd-border rounded text-[10px]"
                    >⌘</kbd
                >
                <kbd
                    class="px-1.5 py-0.5 bg-fd-accent border border-fd-border rounded text-[10px]"
                    >K</kbd
                > Để tìm kiếm thông tin bất kì trong lý thuyết
            </p>
        </div>

        <div
            class="fd-card group hover:border-fd-primary/50 transition-all duration-500"
        >
            <div
                class="w-12 h-12 bg-fd-primary/10 rounded-xl flex items-center justify-center text-fd-primary mb-6 group-hover:scale-110 transition-transform"
            >
                <i class="bx bxs-bot text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">Humain AI</h3>
            <p class="text-sm text-fd-muted font-medium">
                Nhấn vào icon bot để hỏi câu hỏi hoặc tìm kiếm thông tin, bot sẽ
                trả lời cho bạn một cách nhanh chóng và chính sác nhất có thể
            </p>
        </div>

        <div
            class="fd-card group hover:border-fd-primary/50 transition-all duration-500"
        >
            <div
                class="w-12 h-12 bg-fd-primary/10 rounded-xl flex items-center justify-center text-fd-primary mb-6 group-hover:scale-110 transition-transform"
            >
                <i class="bx bx-reflect-horizontal text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">Tương tác</h3>
            <p class="text-sm text-fd-muted font-medium">
                Tương tác động với người dùng thông qua các công cụ tích hợp và
                khả năng xử lý dữ liệu thời gian thực, giúp tạo ra trải nghiệm
                phản hồi nhanh chóng và tự nhiên.
            </p>
        </div>
    </div>
</div>
