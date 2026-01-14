<script>
    import { getContext } from "svelte";
    let { data } = $props();

    const settings = getContext("theorySettings");
</script>

<div
    class="prose prose-lg max-w-4xl mx-auto transition-all duration-200"
    style:font-size="{settings.fontSize}px"
    style:font-family={settings.fontFamily === "sans"
        ? "ui-sans-serif, system-ui, sans-serif"
        : settings.fontFamily === "serif"
          ? "ui-serif, Georgia, serif"
          : "ui-monospace, monospace"}
>
    <h1 class="text-3xl font-bold text-love mb-4">{data.meta.title}</h1>
    <article class="text-text">
        <data.content />
    </article>
</div>

<style>
    /* Custom Prose adaptation for Rosé Pine */
    :global(.prose h1, .prose h2, .prose h3, .prose h4) {
        color: var(--love);
    }
    :global(.prose strong) {
        color: var(--iris);
    }
    :global(.prose blockquote) {
        border-left-color: var(--gold);
        color: var(--subtle);
        font-style: italic;
    }
    :global(.prose a) {
        color: var(--pine);
        text-decoration: none;
    }
    :global(.prose a:hover) {
        text-decoration: underline;
    }
</style>
