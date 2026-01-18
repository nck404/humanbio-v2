<script>
    import { auth, logout } from "$lib/stores/auth";
    import { settings } from "$lib/stores/settings";
    import { page } from "$app/stores";
    import { fade, slide, scale } from "svelte/transition";
    import { isChatOpen } from "$lib/stores/ui";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { API_URL } from "$lib/constants";

    let { user } = $derived($auth);

    let isUserMenuOpen = $state(false);
    let isSettingsOpen = $state(false);

    function toggleUserMenu() {
        isUserMenuOpen = !isUserMenuOpen;
    }

    function toggleSettings() {
        isSettingsOpen = !isSettingsOpen;
    }

    function setTheme(newTheme) {
        settings.update((s) => ({ ...s, theme: newTheme }));
    }

    function setFontFamily(newFont) {
        settings.update((s) => ({ ...s, fontFamily: newFont }));
    }

    function setFontSize(newSize) {
        settings.update((s) => ({ ...s, fontSize: newSize }));
    }

    let syncTimeout;

    async function syncSettings() {
        if ($auth.isAuthenticated) {
            try {
                // Clear any existing timeout
                if (syncTimeout) clearTimeout(syncTimeout);

                // Debounce sync for 1 second
                syncTimeout = setTimeout(async () => {
                    await fetch(`${API_URL}/api/me/settings`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${$auth.token}`,
                        },
                        body: JSON.stringify({ settings: $settings }),
                    });
                }, 1000);
            } catch (e) {
                console.error("Failed to sync settings", e);
            }
        }
    }

    // Auto-sync settings change to backend
    $effect(() => {
        // We need to access $settings properties to track them
        const { primaryColor, fontSize, fontFamily } = $settings;
        syncSettings();
    });

    function handleColorPick(hex) {
        settings.update((s) => ({ ...s, primaryColor: hex }));
    }
</script>

<nav class="sticky top-0 z-[100] glass border-b border-fd-border h-11">
    <div
        class="max-w-[1400px] mx-auto h-full flex items-center justify-between px-4 md:px-5"
    >
        <div class="flex items-center gap-6">
            <a href="/" class="flex items-center gap-2 group">
                <div
                    class="w-6 h-6 bg-fd-primary rounded-sm flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform"
                >
                    <i class="bx bxs-component text-white text-base"></i>
                </div>
                <span
                    class="text-xs font-bold tracking-tight text-fd-foreground hidden sm:block"
                    >HumanBio</span
                >
            </a>

            <div class="hidden md:flex items-center gap-8">
                <a
                    href="/theory"
                    class="relative text-[13px] transition-all px-4 py-1.5 rounded-lg group {$page.url.pathname.startsWith(
                        '/theory',
                    )
                        ? 'text-fd-primary bg-fd-primary/8 font-bold'
                        : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent font-bold'}"
                >
                    Lý thuyết
                    {#if $page.url.pathname.startsWith("/theory")}
                        <div
                            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-fd-primary rounded-full shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                    {/if}
                </a>
                <a
                    href="/tests"
                    class="relative text-[13px] transition-all px-4 py-1.5 rounded-lg group {$page.url.pathname.startsWith(
                        '/tests',
                    )
                        ? 'text-fd-primary bg-fd-primary/8 font-bold'
                        : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent font-bold'}"
                >
                    Kiểm tra
                    {#if $page.url.pathname.startsWith("/tests")}
                        <div
                            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-fd-primary rounded-full shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                    {/if}
                </a>
                <a
                    href="/forum"
                    class="relative text-[13px] transition-all px-4 py-1.5 rounded-lg group {$page.url.pathname.startsWith(
                        '/forum',
                    )
                        ? 'text-fd-primary bg-fd-primary/8 font-bold'
                        : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent font-bold'}"
                >
                    Diễn đàn
                    {#if $page.url.pathname.startsWith("/forum")}
                        <div
                            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-fd-primary rounded-full shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                    {/if}
                </a>
                <a
                    href="/atlas"
                    class="relative text-[13px] transition-all px-4 py-1.5 rounded-lg group {$page.url.pathname.startsWith(
                        '/atlas',
                    )
                        ? 'text-fd-primary bg-fd-primary/8 font-bold'
                        : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent font-bold'}"
                >
                    Giải phẫu
                    {#if $page.url.pathname.startsWith("/atlas")}
                        <div
                            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-fd-primary rounded-full shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                    {/if}
                </a>
                <a
                    href="/rules"
                    class="relative text-[13px] transition-all px-4 py-1.5 rounded-lg group {$page.url.pathname.startsWith(
                        '/rules',
                    )
                        ? 'text-fd-primary bg-fd-primary/8 font-bold'
                        : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent font-bold'}"
                >
                    Quy tắc
                    {#if $page.url.pathname.startsWith("/rules")}
                        <div
                            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-fd-primary rounded-full shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                    {/if}
                </a>
            </div>
        </div>

        <div class="flex items-center gap-2">
            <!-- Chat AI Toggle -->
            <button
                onclick={() => ($isChatOpen = !$isChatOpen)}
                class="p-1.5 text-fd-muted hover:text-fd-foreground hover:bg-fd-accent rounded-md transition-all relative"
                aria-label="Mở Chat AI"
                title="Chat AI"
            >
                <i class="bx bx-message-square-dots text-lg"></i>
                {#if $isChatOpen}
                    <div
                        class="absolute top-1 right-1 w-1.5 h-1.5 bg-fd-primary rounded-full border border-white"
                    ></div>
                {/if}
            </button>

            <!-- Settings Toggle -->
            <button
                onclick={() => (isSettingsOpen = !isSettingsOpen)}
                class="p-1.5 text-fd-muted hover:text-fd-foreground hover:bg-fd-accent rounded-md transition-all"
                aria-label="Cài đặt giao diện"
                title="Giao diện"
            >
                <i class="bx bx-cog text-lg"></i>
            </button>

            <div class="h-4 w-px bg-fd-border mx-0.5 opacity-50"></div>

            {#if $auth.isAuthenticated}
                <div class="relative">
                    <button
                        onclick={() => (isUserMenuOpen = !isUserMenuOpen)}
                        class="flex items-center gap-2 px-1.5 py-1 rounded-sm hover:bg-fd-accent transition-all group border border-transparent hover:border-fd-border"
                        aria-label="Menu người dùng"
                        aria-expanded={isUserMenuOpen}
                    >
                        <Avatar
                            url={user?.avatar_url}
                            seed={user?.avatar_seed || user?.username}
                            size={22}
                            class="rounded-sm shadow-inner"
                        />
                        <span
                            class="text-[11px] font-semibold text-fd-muted group-hover:text-fd-foreground line-clamp-1 max-w-[80px]"
                            >{user?.username}</span
                        >
                        <i
                            class="bx bx-chevron-down text-fd-muted text-[10px] transition-transform {isUserMenuOpen
                                ? 'rotate-180'
                                : ''}"
                        ></i>
                    </button>

                    {#if isUserMenuOpen}
                        <button
                            class="fixed inset-0 z-0 cursor-default"
                            onclick={() => (isUserMenuOpen = false)}
                            aria-label="Đóng menu"
                        ></button>
                        <div
                            transition:slide={{ duration: 150 }}
                            class="absolute right-0 mt-2 w-56 glass border border-fd-border rounded-xl shadow-2xl p-2 z-[110] flex flex-col gap-1"
                        >
                            <div
                                class="flex items-center gap-3 px-3 py-3 border-b border-fd-border mb-1 bg-fd-primary/5 rounded-t-lg"
                            >
                                <Avatar
                                    url={user?.avatar_url}
                                    seed={user?.avatar_seed || user?.username}
                                    size={36}
                                    class="rounded-lg shadow-sm"
                                />
                                <div class="flex flex-col">
                                    <span
                                        class="text-xs font-black text-fd-foreground"
                                        >{user?.username}</span
                                    >
                                    <span
                                        class="text-[9px] font-bold text-fd-primary uppercase tracking-widest"
                                        >Thành viên tích cực</span
                                    >
                                </div>
                            </div>

                            <a
                                href="/profile"
                                class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] text-fd-muted hover:text-fd-foreground hover:bg-fd-accent transition-colors"
                            >
                                <i class="bx bx-user-circle text-base"></i>
                                Hồ sơ cá nhân
                            </a>

                            {#if $auth.user?.is_admin}
                                <div class="h-px bg-fd-border my-1 mx-2"></div>
                                <div
                                    class="px-3 py-1 text-[9px] font-black text-fd-muted uppercase tracking-widest opacity-60"
                                >
                                    Quản trị hệ thống
                                </div>
                                <a
                                    href="/admin"
                                    class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] text-fd-primary hover:bg-fd-primary/10 transition-colors"
                                >
                                    <i class="bx bx-shield-quarter text-base"
                                    ></i>
                                    Trung tâm quản trị
                                </a>
                                <a
                                    href="/admin/tests/new"
                                    class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] text-fd-muted hover:text-fd-foreground hover:bg-fd-accent transition-colors"
                                >
                                    <i class="bx bx-plus-circle text-base"></i>
                                    Tạo bài thi thử
                                </a>
                            {/if}

                            <div class="h-px bg-fd-border my-1 mx-2"></div>

                            <button
                                onclick={logout}
                                class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] text-red-500 hover:bg-red-500/10 transition-colors text-left w-full font-bold"
                            >
                                <i class="bx bx-log-out text-base"></i>
                                Đăng xuất
                            </button>
                        </div>
                    {/if}
                </div>
            {:else}
                <div class="flex items-center gap-1.5">
                    <a
                        href="/login"
                        class="text-[13px] font-medium text-fd-muted hover:text-fd-foreground transition-all px-3 py-1.5"
                    >
                        Đăng nhập
                    </a>
                    <a
                        href="/register"
                        class="fd-btn-primary !text-[11px] !py-1 px-4 !rounded-[6px]"
                    >
                        Tham gia ngay
                    </a>
                </div>
            {/if}
        </div>
    </div>
</nav>

<!-- Global Settings Panel -->
{#if isSettingsOpen}
    <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <button
            transition:fade={{ duration: 200 }}
            class="absolute inset-0 bg-black/60 backdrop-blur-md cursor-default w-full h-full border-none"
            onclick={toggleSettings}
            aria-label="Đóng cài đặt"
        ></button>

        <div
            transition:scale={{ duration: 400, start: 0.9, opacity: 0 }}
            class="relative w-full max-w-sm glass border border-fd-border/50 !rounded-[2.5rem] shadow-2xl p-8 flex flex-col gap-8 overflow-hidden bg-white/80"
        >
            <!-- Decorative Background Glow -->
            <div
                class="absolute -top-24 -right-24 w-48 h-48 rounded-full blur-[80px] opacity-20"
                style="background: {$settings.primaryColor}"
            ></div>

            <div class="flex items-center justify-between pb-2">
                <div>
                    <h3
                        class="text-2xl font-[900] text-fd-foreground tracking-tighter"
                    >
                        Tùy chọn<span class="text-fd-primary">.</span>
                    </h3>
                    <p
                        class="text-[10px] font-bold text-fd-muted uppercase tracking-widest opacity-60"
                    >
                        Cá nhân hóa hệ thống
                    </p>
                </div>
                <button
                    onclick={toggleSettings}
                    class="w-10 h-10 rounded-full hover:bg-fd-secondary flex items-center justify-center transition-all text-fd-muted hover:text-fd-foreground"
                    aria-label="Đóng"
                >
                    <i class="bx bx-x text-2xl"></i>
                </button>
            </div>

            <!-- Interface Color Adjustment -->
            <div class="space-y-6">
                <div class="flex items-center justify-between">
                    <div class="space-y-1">
                        <span
                            class="text-xs font-black text-fd-foreground uppercase tracking-tight"
                            >Main color</span
                        >
                        <p class="text-[11px] text-fd-muted font-medium">
                            chọn màu mà bạn thích
                        </p>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="relative group">
                        <input
                            id="color-picker"
                            type="color"
                            class="w-16 h-16 rounded-2xl cursor-pointer border-4 border-white shadow-2xl transition-all hover:scale-105 p-0 overflow-hidden bg-transparent"
                            value={$settings.primaryColor}
                            oninput={(e) => handleColorPick(e.target.value)}
                        />
                        <div
                            class="absolute -bottom-1 -right-1 w-6 h-6 bg-white rounded-lg shadow-md flex items-center justify-center pointer-events-none border border-fd-border"
                        >
                            <i class="bx bx-eyedropper text-xs text-fd-primary"
                            ></i>
                        </div>
                    </div>

                    <div class="flex-1 grid grid-cols-4 gap-2">
                        {#each ["#6366f1", "#f43f5e", "#10b981", "#0ea5e9", "#f59e0b", "#8b5cf6", "#ec4899", "#3b82f6"] as color}
                            <button
                                onclick={() => handleColorPick(color)}
                                class="w-full aspect-square rounded-xl border-2 transition-all {$settings.primaryColor ===
                                color
                                    ? 'border-fd-primary scale-110 shadow-lg'
                                    : 'border-transparent hover:scale-105'}"
                                style="background-color: {color}"
                                aria-label="Chọn màu {color}"
                            ></button>
                        {/each}
                    </div>
                </div>
            </div>

            <!-- Typography & Size -->
            <div class="space-y-6 pt-4 border-t border-fd-border/30">
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <span
                            class="text-xs font-black text-fd-foreground uppercase tracking-tight"
                            >Kích thước hiển thị</span
                        >
                        <span
                            class="text-[11px] font-black text-fd-primary px-2 py-0.5 bg-fd-primary/10 rounded-md"
                            >{$settings.fontSize}px</span
                        >
                    </div>
                    <div class="px-1">
                        <input
                            type="range"
                            min="12"
                            max="20"
                            step="1"
                            bind:value={$settings.fontSize}
                            class="w-full h-1.5 bg-fd-secondary rounded-full appearance-none cursor-pointer accent-fd-primary"
                        />
                        <div
                            class="flex justify-between mt-2 text-[10px] font-bold text-fd-muted opacity-40 px-1"
                        >
                            <span>GỌN GÀNG</span>
                            <span>THOẢI MÁI</span>
                        </div>
                    </div>
                </div>

                <div class="space-y-3">
                    <span
                        class="text-xs font-black text-fd-foreground uppercase tracking-tight"
                        >Hệ thống phông chữ</span
                    >
                    <div
                        class="grid grid-cols-3 gap-2 p-1 bg-fd-secondary/30 rounded-2xl border border-fd-border/50"
                    >
                        {#each ["sans", "serif", "mono"] as font}
                            <button
                                onclick={() => setFontFamily(font)}
                                class="py-2.5 text-[11px] font-black rounded-xl transition-all uppercase tracking-widest {$settings.fontFamily ===
                                font
                                    ? 'bg-white text-fd-primary shadow-sm border border-fd-border/50 translate-y-[-1px]'
                                    : 'text-fd-muted hover:text-fd-foreground hover:bg-white/50'}"
                            >
                                {font === "sans"
                                    ? "Normal"
                                    : font === "serif"
                                      ? "Thư pháp"
                                      : "Monospace"}
                            </button>
                        {/each}
                    </div>
                </div>
            </div>

            <div class="mt-2 text-center">
                <p
                    class="text-[9px] font-bold text-fd-muted uppercase tracking-[0.2em] opacity-40"
                >
                    Mọi thay đổi sẽ được đồng bộ tự động
                </p>
            </div>
        </div>
    </div>
{/if}
