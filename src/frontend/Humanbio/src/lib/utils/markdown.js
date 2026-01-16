export function renderMarkdown(text) {
    if (!text) return "";
    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "<br/>");

    // Images: ![alt](url)
    html = html.replace(
        /!\[(.*?)\]\((.*?)\)/g,
        '<img src="$2" alt="$1" class="rounded-xl my-4 max-h-[500px] w-auto shadow-lg border border-fd-border/50" />',
    );

    // Links: [text](url)
    html = html.replace(
        /\[(.*?)\]\((.*?)\)/g,
        '<a href="$2" target="_blank" class="text-fd-primary hover:underline font-bold">$1</a>',
    );

    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Italic: *text*
    html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");

    return html;
}

export function stripMarkdown(text) {
    if (!text) return "";
    return text
        .replace(/!\[.*?\]\(.*?\)/g, "") // Remove images
        .replace(/\[(.*?)\]\(.*?\)/g, "$1") // Remove links but keep text
        .replace(/\*\*(.*?)\*\*/g, "$1") // Remove bold
        .replace(/\*(.*?)\*/g, "$1") // Remove italic
        .replace(/`{1,3}.*?`{1,3}/g, "") // Remove code blocks
        .replace(/<.*?>/g, ""); // Remove HTML tags
}
