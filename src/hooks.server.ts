import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	let userid = event.cookies.get('userid');
	// eslint-disable-next-line prefer-const
	let MoodleSession = event.cookies.get('MoodleSession');

	if (!userid) {
		// if this is the first time the user has visited this app,
		// set a cookie so that we recognise them when they return
		userid = crypto.randomUUID();
		event.cookies.set('userid', userid, { path: '/' });
	}

	event.locals.userid = userid;
	event.locals.MoodleSession = MoodleSession;

	return resolve(event);
};
