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
            Knowledge Base
        </div>
        <h1
            class="text-5xl md:text-6xl font-black tracking-tight text-fd-foreground mb-6"
        >
            Master Human <span class="text-gradient">Biology</span>
        </h1>
        <p class="text-lg text-fd-muted leading-relaxed max-w-2xl mx-auto">
            Explore deep dives into physiology, genetics, and anatomy. Selective
            insights categorized for efficient learning and rapid mastery.
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
            <h3 class="text-xl font-bold mb-2">Structured Path</h3>
            <p class="text-sm text-fd-muted font-medium">
                Use the sidebar to navigate through hierarchical lessons
                designed by experts.
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
                Press <kbd
                    class="px-1.5 py-0.5 bg-fd-accent border border-fd-border rounded text-[10px]"
                    >⌘</kbd
                >
                <kbd
                    class="px-1.5 py-0.5 bg-fd-accent border border-fd-border rounded text-[10px]"
                    >K</kbd
                > to find content across the entire library instantly.
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
            <h3 class="text-xl font-bold mb-2">AI Tutoring</h3>
            <p class="text-sm text-fd-muted font-medium">
                Stuck on a concept? Click the bot icon in the toolbar to ask our
                biological assistant.
            </p>
        </div>

        <div
            class="fd-card group hover:border-fd-primary/50 transition-all duration-500"
        >
            <div
                class="w-12 h-12 bg-fd-primary/10 rounded-xl flex items-center justify-center text-fd-primary mb-6 group-hover:scale-110 transition-transform"
            >
                <i class="bx bxs-highlighter text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">Interactivity</h3>
            <p class="text-sm text-fd-muted font-medium">
                Highlight text, take notes, and interact with diagrams directly
                in your browser.
            </p>
        </div>
    </div>
</div>
