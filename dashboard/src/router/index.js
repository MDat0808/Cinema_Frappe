import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Test from "../views/Test.vue";
import Test2 from "../views/Test2.vue";

const router = createRouter({
	history: createWebHistory("/cinemax"),
	routes: [
		{ path: "/", redirect: "/dashboard" },
		{ path: "/dashboard", component: Home },
		{ path: "/about", component: About },
		{ path: "/test", component: Test },
		{ path: "/test2", component: Test2 },
	],
});

export default router;
