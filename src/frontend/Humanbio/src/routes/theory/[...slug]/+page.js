import { error } from '@sveltejs/kit';

/** @type {import('./$types').EntryGenerator} */
export function entries() {
    const modules = import.meta.glob('$lib/content/theory/**/*.md');
    const entriesList = [];
    
    for (const path in modules) {
        // /src/lib/content/theory/basics/intro.md -> basics/intro
        const relativePath = path.split('/theory/')[1];
        const slug = relativePath.replace('.md', '');
        entriesList.push({ slug: slug });
    }
    return entriesList;
}

export async function load({ params }) {
    // Get all markdown files
    const modules = import.meta.glob('$lib/content/theory/**/*.md');
    
    // Construct the expected path suffix found in the glob keys
    // glob keys are like: /src/lib/content/theory/advanced/cells.md
    // params.slug is: advanced/cells
    let matchPath = null;
    
    for (const path in modules) {
        if (path.endsWith(`/${params.slug}.md`)) {
            matchPath = path;
            break;
        }
    }

	if (matchPath) {
        const post = await modules[matchPath]();
		return {
			content: post.default,
			meta: post.metadata,
            slug: params.slug
		};
	} else {
		throw error(404, `Could not find lesson: ${params.slug}`);
	}
}
