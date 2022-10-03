<script lang="ts">
let clazz: string = '';
	export let styled: any = true;
	export let icon: string = '';
	export let header: string;
	export { clazz as class };
</script>

{#if styled === true}
	<div
		class="rounded-[0.25rem] overflow-hidden {clazz}"
		style="box-shadow: 0 0 1rem rgba(0, 0, 0, 0.2)"
	>
		<div class="border-t-[0.25rem] p-4 flex flex-col gap-[2em] h-full" style="border-color: #cc2a49">
			<h1 class="text-4xl my-[1rem] flex items-center gap-[1em]">
				{header}<i class="bx {icon}" />
			</h1>
			<slot />
		</div>
	</div>
{:else}
	<div
		class="border-b-[1px] gap-[2em] flex flex-col non-styled {clazz}"
		style="border-image: linear-gradient(135deg, #582841, #f36f38) 1"
	>
		<h1 class="text-4xl my-[1rem] flex items-center gap-[0.5em]">
			{header}<i class="bx {icon}" />
		</h1>
		<slot />
	</div>
{/if}
