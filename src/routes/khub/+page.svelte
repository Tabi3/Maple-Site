<script lang="js">
	import Navbar from '../../components/Navbar.svelte';
	import Banner from '../../components/Banner.svelte';
	import Textbox from '../../components/Textbox.svelte';
	import Footer from '../../components/Footer.svelte';

	export /**
	 * @type {{ data: { user: { 
				name: undefined; 
				login: { [x: string]: any; }; 
				info: { [x: string]: any; }; 
				badges: any; }; home: any; }; 
		}}
	 */
	 let data;
	console.log(data);

	let logout = () => {
		document.cookie = "MoodleSession=0"
		location.reload()
	}

</script>

<Navbar />
<main class="grid grid-cols-2 gap-[5vw] pt-[4em]">
	{#if data.data.user.name === undefined}
	<Textbox header="PSHS Knowledge hub" class="col-span-2 min-h-[50vh]">	
		<p>
			PSHS Knowledge hub (A.K.A KHUB) is a website that contains the modules for each subject you're
			currently enrolled in.
		</p>
		<p>Currently, You're not logged in</p>
		<div class="w-fit rounded-lg overflow-hidden text-white hover:text-black mt-auto">
			<a href="./login" class=" bg-[#ef4648] flex items-center gap-[0.5em] text-md hl p-[1em]">
				<i class="bx bxs-graduation text-xl" /> Click here to Log in
			</a>
		</div>
	</Textbox>
	{:else}
	<Textbox header="PSHS Knowledge hub">
		<table class="w-full border-spacing-1 border-collapse
					  info-table bg-transparent text-sm font-bold">
			<tr>
				<td>First access to site</td>
				<td>{data.data.user.login["First access to site"]}</td>
			</tr>
			<tr>
				<td>Last access to site</td>
				<td>{data.data.user.login["Last access to site"]}</td>
			</tr>
		</table>
			<div class="grid items-center grid-cols-[7fr_5fr]">		
				<p>Currently, You are logged in as: <br/>
					<strong>{data.data.user.name}</strong>
				</p> 
				<button class="bg-[#ef4648] flex items-center gap-[0.5em] text-md hl p-[1em] mx-4"
						on:click={logout}>
					<i class="bx bxs-log-out text-xl" />Click here to log out
				</button>
			</div>
			<div class="border-l-[0.25em] border-[#ef4648] pl-[1em] rounded-[0.25em] pr-[1em]"
				 style="background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1))">
				<table class="w-full border-spacing-1 border-collapse
							  info-table bg-transparent">
					<tr>
						<td class="w-min">City/Town</td>
						<td>{data.data.user.info["City/town"]}</td>
					</tr>
					<tr>
						<td>Country</td>
						<td>{data.data.user.info["Country"]}</td>
					</tr>
					<tr>
						<td>Email address</td>
						<td>{data.data.user.info["Email address"]}</td>
					</tr>
				</table>
			</div>
			<h1 class="flex items-center gap-[0.5em] text-md text-xl">Badges <i class="bx bxs-graduation"></i></h1>
			<ul class="border-l-[0.25em] border-[#ef4648] pl-[2em] rounded-[0.25em] flex 
				   	   overflow-scroll badges gap-4 py-4">
			{#each data.data.user.badges as badge, i}
				{@html badge}
			{/each}
		</ul>
	</Textbox>		
	<Textbox header="My courses" styled="false" class="pb-4 relative">
		<div class="flex flex-col h-[calc(100%_-_7.25em)] w-full overflow-y-scroll absolute 
					top-[4.75em] !bg-transparent gap-6 p-2">
			{#each data.data.home as i, j}
			<a href={i[0].link} class="">
				<div class="p-4 grid rounded-[1em] min-h-[15em] overflow-hidden shadow-mine hover:scale-[1.01]"
					 style="grid-template-columns: 2fr 1fr">
					<div class="flex flex-col gap-2 relative">
						<h1>{i[0].title}</h1>
						<div class="flex gap-2">
							{#each i[0].advisers as k, l}
								<a href={k.profile} title={k.name} 
								class="rounded-full overflow-hidden h-10 w-10">
									<img src={k.pfp} alt="">
								</a>
							{/each}
						</div>
						<div class="w-full !bg-transparent px-[50%] absolute py-[5em] top-20 z-10 fades" />
						<div class="overflow-y-scroll absolute !bg-transparent top-20 w-full h-[calc(100%_-_5em)] grid">
							<div>
								{@html i[0].description}	
							</div>
						</div>
					</div>
					<img src={i[0].img} alt="" class="aspect-[316_/_211] object-cover -mt-4 ml-4 bg-white"
						style="height: calc(100% + 2em)">
				</div>
			</a>
			
			{/each}
		</div>
	</Textbox>
	<Textbox header="Coming Soon..." class="col-span-2" icon="">
	</Textbox>			
	{/if}
	
</main>
<Footer />
