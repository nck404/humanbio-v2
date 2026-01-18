<script>
    let { onOpenSearch, onToggleSidebar, onOpenChat } = $props();
</script>

<nav
    class="sticky top-11 z-[40] glass border-b border-fd-border h-11 transition-all duration-300"
>
    <div
        class="max-w-[1400px] mx-auto h-full flex items-center justify-between px-4 md:px-5"
    >
        <div class="flex items-center gap-3">
            <!-- Mobile Toggle -->
            <button
                onclick={onToggleSidebar}
                class="lg:hidden text-fd-muted hover:text-fd-primary p-1.5 hover:bg-fd-primary/10 rounded-md transition-all"
                aria-label="Toggle Navigation"
            >
                <i class="bx bx-menu text-xl"></i>
            </button>

            <!-- Breadcrumbs -->
            <div
                class="flex items-center gap-2 text-[11px] font-black text-fd-muted-foreground mr-4"
            >
                <span
                    class="text-white bg-fd-primary px-3 py-1 rounded-full shadow-lg shadow-fd-primary/20 scale-105"
                    >Lý thuyết</span
                >
                <i class="bx bx-chevron-right opacity-30 text-xs"></i>
                <span
                    class="line-clamp-1 max-w-[150px] text-fd-foreground bg-fd-secondary px-3 py-1 rounded-full border border-fd-border font-bold"
                    >Sinh học</span
                >
            </div>
        </div>

        <div class="flex items-center gap-3">
            <button
                onclick={onOpenSearch}
                class="flex items-center gap-2 px-3 py-1.5 bg-fd-secondary/40 border border-fd-border rounded-lg hover:border-fd-primary/30 hover:bg-white hover:shadow-lg hover:shadow-fd-primary/5 transition-all group relative overflow-hidden"
                aria-label="Search Documentation"
            >
                <i
                    class="bx bx-search text-fd-muted group-hover:text-fd-primary text-sm transition-colors"
                ></i>
                <span
                    class="text-[10px] font-extrabold text-fd-muted group-hover:text-fd-foreground hidden sm:inline"
                    >Search Library...</span
                >
                <div
                    class="hidden sm:flex items-center gap-1 text-[8px] text-fd-muted-foreground ml-3"
                >
                    <kbd
                        class="bg-fd-accent px-1.5 py-0.5 rounded border border-fd-border font-sans font-black opacity-60"
                        >⌘</kbd
                    >
                    <kbd
                        class="bg-fd-accent px-1.5 py-0.5 rounded border border-fd-border font-sans font-black opacity-60"
                        >K</kbd
                    >
                </div>
            </button>

            <div class="h-4 w-px bg-fd-border mx-1 opacity-50"></div>

            <button
                onclick={onOpenChat}
                class="p-1.5 text-fd-muted hover:text-white hover:bg-fd-primary rounded-lg transition-all relative group"
                aria-label="Ask AI Assistant"
            >
                <i class="bx bxs-bot text-lg relative z-10"></i>
                <span
                    class="absolute inset-0 bg-fd-primary rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
                ></span>
                <span
                    class="absolute top-1 right-1 w-2 h-2 bg-fd-primary border-2 border-white rounded-full shadow-[0_0_10px_var(--primary-glow)] animate-pulse"
                ></span>
            </button>
        </div>
    </div>
</nav>
