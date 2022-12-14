import type * as Kit from '@sveltejs/kit';

type Expand<T> = T extends infer O ? { [K in keyof O]: O[K] } : never;
type RouteParams = {  }
type MaybeWithVoid<T> = {} extends T ? T | void : T;
export type RequiredKeys<T> = { [K in keyof T]-?: {} extends { [P in K]: T[K] } ? never : K; }[keyof T];
type OutputDataShape<T> = MaybeWithVoid<Omit<App.PageData, RequiredKeys<T>> & Partial<Pick<App.PageData, keyof T & keyof App.PageData>> & Record<string, any>>
type EnsureParentData<T> = T extends null | undefined ? {} : T;
type PageServerParentData = Omit<EnsureParentData<import('../$types.js').LayoutServerData>, keyof LayoutServerData> & EnsureParentData<LayoutServerData>;
type PageParentData = Omit<EnsureParentData<import('../$types.js').LayoutData>, keyof LayoutData> & EnsureParentData<LayoutData>;
type LayoutParams = RouteParams & {  }
type LayoutParentData = EnsureParentData<import('../$types.js').LayoutData>;

export type PageServerLoad<OutputData extends OutputDataShape<PageServerParentData> = OutputDataShape<PageServerParentData>> = Kit.ServerLoad<RouteParams, PageServerParentData, OutputData>;
export type PageServerLoadEvent = Parameters<PageServerLoad>[0];
export type ActionData = unknown;
export type PageServerData = Expand<Kit.AwaitedProperties<Awaited<ReturnType<typeof import('./proxy+page.server.js').load>>>>;
export type PageData = Expand<Omit<PageParentData, keyof PageServerData> & PageServerData>;
export type Action = Kit.Action<RouteParams>
export type Actions = Kit.Actions<RouteParams>
export type LayoutServerData = null;
export type LayoutData = Expand<LayoutParentData>;
export type RequestEvent = Kit.RequestEvent<RouteParams>;