<script>
    import { settings } from "$lib/stores/settings";
    import { fade, fly } from "svelte/transition";
</script>

<div
    class="relative min-h-[calc(100vh-2.75rem)] flex items-center overflow-hidden mesh-gradient pb-20"
>
    <!-- Rich Dynamic Mesh Backgrounds tied to primaryHue -->
    <div
        class="absolute top-[-10%] left-[-5%] w-[60%] h-[60%] rounded-full blur-[120px] opacity-[0.25] pointer-events-none transition-colors duration-1000"
        style="background: radial-gradient(circle, var(--primary), transparent)"
    ></div>
    <div
        class="absolute bottom-[-10%] right-[-5%] w-[50%] h-[50%] rounded-full blur-[100px] opacity-[0.2] pointer-events-none transition-colors duration-1000"
        style="background: radial-gradient(circle, var(--secondary), transparent)"
    ></div>

    <!-- Decorative floating elements (Biology theme) -->
    <div
        class="absolute inset-0 pointer-events-none overflow-hidden opacity-30"
    >
        {#each Array(6) as _, i}
            <div
                class="absolute rounded-full border border-fd-primary/20 blur-[2px] animate-float"
                style="
                    width: {40 + i * 20}px; 
                    height: {40 + i * 20}px; 
                    top: {15 + i * 12}%; 
                    left: {10 + i * 15}%;
                    animation-delay: {i * 1.5}s;
                    animation-duration: {15 + i * 2}s;
                "
            ></div>
        {/each}
    </div>

    <div class="max-w-[1400px] mx-auto px-8 py-24 relative z-10 w-full">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div in:fade={{ duration: 800 }}>
                <div
                    class="inline-flex items-center gap-3 px-4 py-2 rounded-full border border-fd-primary/30 bg-fd-primary/10 text-[11px] font-bold uppercase tracking-[0.2em] text-fd-primary mb-10 shadow-lg shadow-fd-primary/10"
                    in:fly={{ y: 20, delay: 200 }}
                >
                    <span class="relative flex h-2 w-2">
                        <span
                            class="animate-ping absolute inline-flex h-full w-full rounded-full bg-fd-primary opacity-75"
                        ></span>
                        <span
                            class="relative inline-flex rounded-full h-2 w-2 bg-fd-primary"
                        ></span>
                    </span>
                    Trí tuệ thế hệ mới • Sinh học người
                </div>

                <h1
                    class="text-6xl md:text-7xl lg:text-9xl font-black tracking-tighter text-fd-foreground mb-10 text-balance leading-[0.85] transition-all"
                    in:fly={{ y: 40, delay: 400 }}
                >
                    Học <span class="text-highlight">Sinh học</span><br />Với sự
                    <span class="relative">
                        Chuẩn xác
                        <div
                            class="absolute -bottom-2 left-0 right-0 h-4 bg-fd-primary/10 -rotate-1 rounded-full -z-10"
                        ></div>
                    </span>
                </h1>

                <p
                    class="text-xl md:text-2xl text-fd-muted mb-14 text-balance leading-relaxed max-w-xl font-medium opacity-90"
                    in:fly={{ y: 40, delay: 600 }}
                >
                    Một <span class="text-highlight"
                        >phòng thí nghiệm cao cấp</span
                    > dành cho việc nghiên cứu sinh học. Giải mã sự phức tạp của
                    sự sống với các công cụ tối tân.
                </p>

                <div
                    class="flex flex-wrap gap-6"
                    in:fly={{ y: 40, delay: 800 }}
                >
                    <a
                        href="/theory"
                        class="fd-btn-primary glow-effect !px-12 !py-5 !text-lg group relative"
                    >
                        <span class="relative z-10 flex items-center gap-3">
                            Bắt đầu học ngay
                            <i
                                class="bx bx-right-arrow-alt text-2xl group-hover:translate-x-2 transition-transform"
                            ></i>
                        </span>
                    </a>
                    <a
                        href="/register"
                        class="px-12 py-5 text-lg font-bold uppercase tracking-wider bg-white/50 backdrop-blur-xl border border-fd-border rounded-xl hover:bg-fd-accent hover:border-fd-primary/40 transition-all shadow-xl hover:-translate-y-1"
                    >
                        Tham gia ngay
                    </a>
                </div>
            </div>

            <div
                class="grid grid-cols-1 sm:grid-cols-2 gap-8"
                in:fly={{ x: 60, delay: 1000 }}
            >
                <!-- Bento 1 -->
                <div
                    class="fd-card !p-10 !rounded-[2.5rem] bg-gradient-to-br from-white to-fd-primary/[0.03] hover:to-fd-primary/10 group cursor-default shadow-2xl transition-all duration-700"
                >
                    <div
                        class="w-16 h-16 bg-fd-primary text-white rounded-2xl flex items-center justify-center mb-8 shadow-2xl shadow-fd-primary/30 group-hover:scale-110 group-hover:rotate-6 transition-all duration-500"
                    >
                        <i class="bx bxs-brain text-4xl"></i>
                    </div>
                    <h3 class="text-3xl font-black mb-4 tracking-tighter">
                        Nơ-ron
                    </h3>
                    <p
                        class="text-fd-muted text-base leading-relaxed font-semibold opacity-70"
                    >
                        Bản đồ lý thuyết thông minh kết nối các khái niệm phức
                        tạp.
                    </p>
                </div>

                <!-- Bento 2 -->
                <div
                    class="fd-card !p-10 !rounded-[2.5rem] bg-gradient-to-br from-white to-emerald-500/[0.03] hover:to-emerald-500/10 group cursor-default mt-0 sm:mt-12 shadow-2xl border-emerald-500/10 transition-all duration-700"
                >
                    <div
                        class="w-16 h-16 bg-emerald-500 text-white rounded-2xl flex items-center justify-center mb-8 shadow-2xl shadow-emerald-500/30 group-hover:scale-110 group-hover:-rotate-6 transition-all duration-500"
                    >
                        <i class="bx bxs-microscope text-4xl"></i>
                    </div>
                    <h3 class="text-3xl font-black mb-4 tracking-tighter">
                        Thực nghiệm
                    </h3>
                    <p
                        class="text-fd-muted text-base leading-relaxed font-semibold opacity-70"
                    >
                        Hệ thống đánh giá độ chính xác cao cho việc làm chủ kiến
                        thức.
                    </p>
                </div>

                <!-- Bento 3 -->
                <div
                    class="fd-card !p-10 !rounded-[2.5rem] bg-gradient-to-br from-white to-amber-500/[0.03] hover:to-amber-500/10 group cursor-default shadow-2xl border-amber-500/10 transition-all duration-700"
                >
                    <div
                        class="w-16 h-16 bg-amber-500 text-white rounded-2xl flex items-center justify-center mb-8 shadow-2xl shadow-amber-500/30 group-hover:scale-110 group-hover:rotate-6 transition-all duration-500"
                    >
                        <i class="bx bxs-palette text-4xl"></i>
                    </div>
                    <h3 class="text-3xl font-black mb-4 tracking-tighter">
                        Sắc thái
                    </h3>
                    <p
                        class="text-fd-muted text-base leading-relaxed font-semibold opacity-70"
                    >
                        Không gian học tập năng động thích ứng với trạng thái
                        của bạn.
                    </p>
                </div>

                <!-- Bento 4 -->
                <div
                    class="fd-card !p-10 !rounded-[2.5rem] bg-gradient-to-br from-white to-rose-500/[0.03] hover:to-rose-500/10 group cursor-default mt-0 sm:mt-12 shadow-2xl border-rose-500/10 transition-all duration-700"
                >
                    <div
                        class="w-16 h-16 bg-rose-500 text-white rounded-2xl flex items-center justify-center mb-8 shadow-2xl shadow-rose-500/30 group-hover:scale-110 group-hover:-rotate-6 transition-all duration-500"
                    >
                        <i class="bx bxs-award text-4xl"></i>
                    </div>
                    <h3 class="text-3xl font-black mb-4 tracking-tighter">
                        Cấp bậc
                    </h3>
                    <p
                        class="text-fd-muted text-base leading-relaxed font-semibold opacity-70"
                    >
                        Gắn huy hiệu chứng nhận cho sự am hiểu sinh học của bạn.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    @keyframes float {
        0%,
        100% {
            transform: translateY(0) rotate(0deg);
        }
        50% {
            transform: translateY(-20px) rotate(10deg);
        }
    }
    .animate-float {
        animation: float infinite ease-in-out;
    }
</style>
