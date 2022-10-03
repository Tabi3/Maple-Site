<script lang="ts">
	import Navbar from '../../components/Navbar.svelte';
	import Textbox from '../../components/Textbox.svelte';
	import Footer from '../../components/Footer.svelte';
	import axios from 'axios'


	let handleForm = (event: any) => {
		const formData = new FormData(event.target);

		const data: any = {};
		for (let field of formData) {
			const [key, value] = field;
			data[key] = value;
		}
		let value: any;
		let promise = axios({
			method: "POST",
			url: 'http://localhost:5000/flask/khub-login',
			data: data
		})
		promise.then((x) => {
			console.log(x.data)
			document.cookie = `MoodleSession=${x.data.cookie}`
		})

		
	};
</script>

<Navbar />
<main class="grid grid-cols-2 gap-[5vw] pt-[4em]">
	<Textbox header="Login Form" class="col-span-2">
		<div class="grid grid-cols-2 gap-4">
			<form on:submit|preventDefault={handleForm} class="flex flex-col gap-4">
				<input
					placeholder="Enter E-mail"
					value=""
					type="email"
					name="email"
					id=""
					class="w-full h-12 dark:bg-[#1B1E21] px-4 border-slate-800 shadow-md rounded-md"
				/>
				<input
					placeholder="Enter Password"
					type="password"
					value=""
					name="password"
					id=""
					class="w-full h-12 dark:bg-[#1B1E21] px-4 border-slate-800 shadow-md rounded-md"
				/>
				<input type="submit" value="Login" class="w-1/4 shadow-md hl" />
			</form>
			<div class="mt-[-7.5rem] m-[-1rem] w-full ml-[1rem] overflow-hidden rounded-l-3xl">
				<img
					src="https://khub.cvc.pshs.edu.ph/theme/image.php/moove/theme/1642486302/headerimg"
					alt=""
					class="blur-md"
				/>
			</div>
		</div>
	</Textbox>
	<Textbox header="Text" />
	<Textbox header="Text" styled="false" />
</main>
<Footer />
