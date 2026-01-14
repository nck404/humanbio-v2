<script>
    import HumanBodySVG from "$lib/components/atlas/HumanBodySVG.svelte";
    import DetailWindow from "$lib/components/atlas/DetailWindow.svelte";
    import { fly } from "svelte/transition";

    let selectedPart = null;

    function handleSelect(event) {
        selectedPart = event.detail;
    }
</script>

<div class="min-h-screen py-10 px-4 md:px-0">
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12" in:fly={{ y: -20, duration: 600 }}>
            <span
                class="text-xs font-black uppercase tracking-[0.3em] text-fd-primary mb-3 block"
                >Mô phỏng 2D</span
            >
            <h1
                class="text-4xl md:text-5xl font-[900] tracking-tighter text-fd-foreground mb-4"
            >
                Bản Đồ Giải Phẫu
                <span class="text-fd-primary">.</span>
            </h1>
            <p
                class="text-fd-muted font-medium max-w-xl mx-auto leading-relaxed"
            >
                Khám phá cấu trúc cơ thể người thông qua mô hình tương tác. Chọn
                các vùng cơ thể để truy cập dữ liệu y khoa chi tiết.
            </p>
        </div>

        <!-- Main Workspace -->
        <div
            class="relative bg-white/5 rounded-[3rem] border border-white/10 p-2 md:p-10 shadow-2xl backdrop-blur-sm overflow-hidden"
            in:fly={{ y: 20, duration: 800, delay: 200 }}
        >
            <!-- Background Glow -->
            <div
                class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-fd-primary/5 rounded-full blur-[120px] pointer-events-none"
            ></div>

            <HumanBodySVG on:select={handleSelect} />

            <!-- Instructions Overlay -->
            <div
                class="absolute bottom-6 left-0 right-0 text-center pointer-events-none opacity-60 mix-blend-overlay"
            >
                <span
                    class="text-[10px] font-black uppercase tracking-widest text-fd-foreground flex items-center justify-center gap-2"
                >
                    <i class="bx bx-mouse-alt animate-bounce"></i>
                    Nhấp vào các vùng để xem chi tiết
                </span>
            </div>
        </div>
    </div>

    <!-- Detail Window (Modal) -->
    <DetailWindow part={selectedPart} on:close={() => (selectedPart = null)} />
</div>
