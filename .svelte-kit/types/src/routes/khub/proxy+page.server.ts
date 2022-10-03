// @ts-nocheck
/* eslint-disable prefer-const */
import type { PageServerLoad } from './$types';
import axios, { type AxiosResponse } from 'axios';
import { error } from '@sveltejs/kit'


type KhubData = {
	courses: Array<{ string: string }>;
	user: { string: Array<string> }
}

export const load = async ({ locals }: Parameters<PageServerLoad>[0]) => {
	let courses: AxiosResponse | void = await axios.get('http://localhost:5000/flask/khub', {
		headers: {
			Cookie: `MoodleSession=${locals.MoodleSession};`
		}
	}).catch(error => { console.error(error) })
	if (courses?.status === 200) {
		return {
			data: courses.data as KhubData[],
		};
	}
	return { data: { user: { name: undefined } } }
};