/**
 * Serve the Interview Prep static book via Workers Assets.
 * Replaces any previous Hello World Worker script.
 */
export default {
  async fetch(request, env) {
    return env.ASSETS.fetch(request);
  },
};
