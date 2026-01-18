<script>
    import { settings } from "$lib/stores/settings";
    import Highlighter from "$lib/components/theory/Highlighter.svelte";
    import Comments from "$lib/components/theory/Comments.svelte";

    let { data } = $props();
</script>

<Highlighter />

<div class="space-y-6">
    <header class="pb-8 border-b border-fd-border">
        <h1
            class="text-4xl font-extrabold text-fd-foreground tracking-tight mb-4"
        >
            {data.meta.title}
        </h1>
        <div class="flex flex-wrap items-center gap-4 text-xs font-bold">
            <div
                class="flex items-center gap-2 text-fd-primary bg-fd-primary/10 px-3 py-1.5 rounded-full"
            >
                <i class="bx bx-time-five"></i>
                <span>Đã cập nhập gần đây</span>
            </div>
            <div
                class="flex items-center gap-2 text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-100"
            >
                <i class="bx bx-book-reader"></i>
                <span>10 phút đọc</span>
            </div>
            <div
                class="flex items-center gap-2 text-amber-600 bg-amber-50 px-3 py-1.5 rounded-full border border-amber-100"
            >
                <i class="bx bx-bar-chart-alt-2"></i>
                <span>Đã được kiểm định bởi hội đồng Admin</span>
            </div>
        </div>
    </header>

    <article class="text-fd-foreground leading-relaxed">
        <data.content />
    </article>

    <Comments slug={data.slug} />
</div>

<style>
    /* Specific prose overrides if needed, otherwise handled by layout */
    :global(.prose article img) {
        border-radius: 0.75rem;
        border: 1px solid var(--border);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
    }
</style>
