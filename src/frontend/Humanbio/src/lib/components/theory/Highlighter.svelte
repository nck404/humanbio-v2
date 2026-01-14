<script>
    import { onMount } from "svelte";

    let selection = null;

    function handleKeydown(event) {
        if (event.ctrlKey && ["1", "2", "3"].includes(event.key)) {
            event.preventDefault();
            applyHighlight(event.key);
        }
    }

    function applyHighlight(key) {
        const sel = window.getSelection();
        if (!sel.rangeCount) return;

        const range = sel.getRangeAt(0);
        const selectedText = range.toString();

        if (!selectedText.trim()) return;

        // Create a wrapper span
        const span = document.createElement("span");
        span.className = `highlight-v${key}`;
        span.textContent = selectedText;

        // Replace selected text with the span
        range.deleteContents();
        range.insertNode(span);

        // Clear selection
        sel.removeAllRanges();
    }
</script>

<svelte:window onkeydown={handleKeydown} />
