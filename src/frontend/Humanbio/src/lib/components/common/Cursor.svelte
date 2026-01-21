<script>
    import { onMount } from "svelte";
    import { spring } from "svelte/motion";

    let coords = spring(
        { x: 0, y: 0 },
        {
            stiffness: 0.15,
            damping: 0.7,
        },
    );

    let size = spring(15, {
        stiffness: 0.2,
        damping: 0.5,
    });

    let isHovering = false;

    let isClicking = false;

    let isVisible = false;

    onMount(() => {
        const handleMouseMove = (e) => {
            isVisible = true;
            coords.set({ x: e.clientX, y: e.clientY });
        };

        const handleMouseOver = (e) => {
            isVisible = true;
            if (
                e.target.tagName === "BUTTON" ||
                e.target.tagName === "A" ||
                e.target.closest("button") ||
                e.target.closest("a") ||
                e.target.classList.contains("cursor-hover")
            ) {
                isHovering = true;
                size.set(50);
            } else {
                isHovering = false;
                size.set(15);
            }
        };

        const handleMouseDown = () => {
            isClicking = true;
            size.set(10);
        };

        const handleMouseUp = () => {
            isClicking = false;
            size.set(isHovering ? 50 : 15);
        };

        const handleMouseLeave = () => {
            isVisible = false;
        };

        const handleMouseOut = (e) => {
            if (!e.relatedTarget && !e.toElement) {
                handleMouseLeave();
            }
        };

        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseover", handleMouseOver);
        window.addEventListener("mousedown", handleMouseDown);
        window.addEventListener("mouseup", handleMouseUp);
        document.addEventListener("mouseout", handleMouseOut);

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("mouseover", handleMouseOver);
            window.removeEventListener("mousedown", handleMouseDown);
            window.removeEventListener("mouseup", handleMouseUp);
            document.removeEventListener("mouseout", handleMouseOut);
        };
    });
</script>

<div
    class="custom-cursor fixed top-0 left-0 pointer-events-none z-[9999] rounded-full mix-blend-difference flex items-center justify-center"
    style="
        transform: translate3d({$coords.x}px, {$coords.y}px, 0) translate(-50%, -50%);
        width: {$size}px;
        height: {$size}px;
        background-color: white; 
        opacity: {isVisible ? 1 : 0};
        transition: opacity 0.3s ease;
    "
></div>

<div
    class="custom-cursor-dot fixed top-0 left-0 pointer-events-none z-[9999] w-2 h-2 bg-fd-primary rounded-full transition-transform duration-75"
    style="
        transform: translate3d({$coords.x}px, {$coords.y}px, 0) translate(-50%, -50%);
        opacity: {isVisible ? 1 : 0};
    "
></div>

<style>
    /* Global Clean up for default cursor if desired, though usually we keep it as fallback 
       or hide it only on body. 
       Adding this to :global(body) { cursor: none; } might be too aggressive, 
       so I'll stick to overlay cursor first. 
    */
    :global(body) {
        cursor: none;
    }

    /* Ensure cursor is visible on top of everything */
    .custom-cursor {
        /* backdrop-filter: invert(1); */
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
</style>
