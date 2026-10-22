import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const ppts = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/ppts' }),
  schema: z.object({
    config: z.record(z.string(), z.any()).optional().default({}),
    decks: z.array(
      z.object({
        template: z.string(),
        slide: z.record(z.string(), z.any()).default({}),
      })
    ),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default(''),
    date: z.coerce.date().optional(),
    author: z.string().optional().default('Eric'),
    tags: z.array(z.string()).optional().default([]),
    cover: z.string().optional(),
  }),
});

export const collections = { ppts, blog };
