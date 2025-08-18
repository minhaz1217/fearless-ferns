// importing a newer version of mermaid that supports new syntax
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.3.0/dist/mermaid.esm.min.mjs";

// All the ramaining code is left unchanged
let is_running = false;
const queue = [];

export default {
  template: `<div></div>`,
  data: () => ({
    last_content: "",
  }),
  mounted() {
    this.initialize();
    this.update(this.content);
  },
  methods: {
    initialize() {
      try {
        mermaid.initialize(this.config || {});
      } catch (error) {
        console.error(error);
        this.$emit("error", error);
      }
    },
    async update(content) {
      if (this.last_content === content) return;
      this.last_content = content;
      queue.push({ element: this.$el, content: content });
      if (is_running) return;
      is_running = true;
      while (queue.length) {
        const { element, content } = queue.shift();
        try {
          const { svg, bindFunctions } = await mermaid.render(element.id + "_mermaid", content);
          element.innerHTML = svg;
          bindFunctions?.(element);
        } catch (error) {
          const { svg, bindFunctions } = await mermaid.render(element.id + "_mermaid", "error");
          element.innerHTML = svg;
          bindFunctions?.(element);
          const mermaidErrorFormat = { str: error.message, message: error.message, hash: error.name, error };
          console.error(mermaidErrorFormat);
          this.$emit("error", mermaidErrorFormat);
        }
      }
      is_running = false;
    },
  },
  props: {
    config: Object,
    content: String,
  },
};