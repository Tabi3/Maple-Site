// @ts-nocheck
import type { PageServerLoad, Actions } from './$types';

export const load = async ({ locals }: Parameters<PageServerLoad>[0]) => {
	return {
		todos: []
	};
};