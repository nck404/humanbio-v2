export const prerender = true;

export async function load() {
	const modules = import.meta.glob('$lib/content/theory/**/*.md');
	const tree = [];

	for (const path in modules) {
		const mod = await modules[path]();
		const metadata = mod.metadata;
		// path examples: 
        // /src/lib/content/theory/basics/intro.md -> slug: basics/intro
        // /src/lib/content/theory/advanced/cells.md -> slug: advanced/cells
        
        const relativePath = path.split('/theory/')[1];
        const parts = relativePath.split('/');
        
        // Handle simple filing system: folders become categories
        // We will build a simple tree: { name: 'basics', children: [...], isFolder: true }
        
        let currentLevel = tree;
        
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const isFile = i === parts.length - 1;
            
            if (isFile) {
                // It's a file
                // Use relative path for slug to ensure consistent routing, ignoring frontmatter slug
                const slug = relativePath.replace('.md', '');
                currentLevel.push({
                    title: metadata.title || part.replace('.md', ''),
                    slug: slug, // This slug should be full path for the router to understand if we change routing logic
                    // Actually, for [slug] route, we might need to handle forward slashes
                    // Let's use the file path logic for slug to be safe: 'basics/intro'
                    // Ensure the route [slug] can match multiple segments or use [...slug]
                     isFolder: false
                });
            } else {
                // It's a folder
                let existingFolder = currentLevel.find(item => item.isFolder && item.name === part);
                if (!existingFolder) {
                    existingFolder = { name: part, isFolder: true, children: [] };
                     currentLevel.push(existingFolder);
                }
                currentLevel = existingFolder.children;
            }
        }
	}

	return {
		tree
	};
}
