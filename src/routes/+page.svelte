<script>
	import Navbar from '../components/Navbar.svelte';
	import Banner from '../components/Banner.svelte';
	import Textbox from '../components/Textbox.svelte';
	import Footer from '../components/Footer.svelte';
	import Khub from '../SRC/Khub.png';
	import Wolframalpha from '../SRC/Wolframalpha.png';

	let username = '';
</script>

<Navbar />
<Banner />
<main class="grid grid-cols-2 gap-[5vw] pt-[4em]">
	<Textbox header="What is Maple?">
		<p>
			Maple is a personal website created by me [Tafí] and is basically just a simple website
			redesign for the following sites...
		</p>
		<ol class="border-l-[0.25em] border-[#ef4648] pl-[2em] rounded-[0.25em] list-decimal">
			<li>PSHS Knowledge Hub</li>
			<li>Wolfram Alpha</li>
		</ol>
		<p>Oh right it also manages the Maple discord bot.</p>
		<div class="w-fit rounded-lg overflow-hidden text-white hover:text-black">
			<a href="./login" class=" bg-[#ef4648] flex items-center gap-[0.5em] text-md hl p-[1em]">
				<i class="bx bxl-discord text-xl" /> Click here to invite Maple
			</a>
		</div>
	</Textbox>
	<Textbox header="Why did I create This website?." styled="false">
		<p>
			I find the UI of some websites bad, therefore I decided to make a website that scrapes
			information from said websites and makes it look better. Examples are listed down below but in
			other words, i made it to make websites to fit my preference.
		</p>
	</Textbox>
	<Textbox header="PSHS Knowledge Hub" icon="bxs-graduation" styled="false">
		<p>
			This website is a Moodle website that contains most if not all information our school provides
			for one school year at a time. The UI is user friendly nowadays, however I am not a fan that
			the UI is very laggy and buggy.	
		</p>
	</Textbox>
	<img
		src={Khub}
		alt="Khub"
		class="aspect-[16/8] overflow-hidden w-full object-cover object-left-top shadow-mine"
	/>
	<Textbox header="Wolfram Alpha" icon="bxs-calculator" styled="false">
		<p>
			This website is basically a calculator website. FYI I do not have premium access so i can't
			show the solutions when solving equations. The reason I redesigned this is so that I can test
			my webscraping capabilities that no joke, works like a charm.
		</p>
	</Textbox>
	<img
		src={Wolframalpha}
		alt="Wolfram"
		class="aspect-[16/8] overflow-hidden w-full object-cover object-left-top shadow-mine"
	/>
</main>
<Footer />
