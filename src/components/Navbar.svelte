<script>
	import { onMount } from 'svelte';
	let darkmode = () => {};
	onMount(() => {
		let html = document.getElementsByTagName('html')[0].classList;
		console.log(localStorage.getItem('dmode'))
		if (localStorage.getItem('dmode') === 'true') {	
			document.getElementsByTagName('html')[0].classList.add('dark');
		}

		darkmode = () => {
			if (html.contains('dark')) {
				localStorage.setItem('dmode', 'false');
				return html.remove('dark');
			}
			localStorage.setItem('dmode', 'true');
			html.add('dark');
		};
	})
	
</script>

<div
	class="text-slate-900 flex flex-row-reverse shadow-lg border-b-[0.25rem] bg-white 
			  nv-bar z-10 fixed w-screen top-0 dark:text-white dark:bg-[#191e22] px-[15vw]"
	style="border-image: linear-gradient(135deg, #582841, #f36f38) 1;"
>
	<ul id="hyperlinks" class="flex flex-row pt-2 pb-2 navbar-hls gap-8">
		<li><a href="/khub">PSHS Knowledge Hub</a></li>
		<li><a href="/wolfram-alpha">Wolfram Alpha</a></li>
		<li><a href="/">Maple Bot</a></li>
	</ul>
	<ul class="items-center flex justify-center w-4 mr-auto">
		<button
			class="bg-slate-500 h-fit aspect-square min-h-[2rem] 
					 rounded-md dark:min-h-[1rem] transition-all duration-[0.2s]"
			on:click={darkmode}
			id="dmode"
		/>
	</ul>
</div>
