<script>
	import SidebarItem from "./SidebarItem.svelte";

	let { tree = [] } = $props();
</script>

<div class="flex flex-col gap-4">
	<!-- Navigation List -->
	<nav class="flex flex-col relative pl-2">
		{#each tree as item}
			<SidebarItem {item} />
		{/each}
	</nav>
</div>
