<template>
  <div class="relative flex flex-col h-full">
    <q-editor
      ref="qRef"
      v-bind="$attrs"
      v-model="inputValue"
      :definitions="{
        save: { tip: 'Save your work', icon: 'save', label: 'Save', handler: saveWork },
        upload: { tip: 'Upload to cloud', icon: 'cloud_upload', label: 'Upload', handler: uploadIt },
        keyboard: { tip: 'Toggle emoji keyboard', icon: 'keyboard', label: 'Emoji', handler: toggleEmojiKeyboard }
      }"
      :toolbar="[ ['bold', 'italic', 'strike', 'underline'], ['keyboard', 'upload', 'save'] ]"
      class="flex-1"
    />

    <!-- Emoji keyboard -->
    <div v-if="emojiKeyboardVisible" class="absolute bottom-0 right-0 left-0 bg-white border-t shadow-lg p-2 flex overflow-x-auto" style="z-index: 1000;">
      <q-btn
        v-for="e in emojis"
        :key="e"
        flat
        size="md"
        class="min-w-[50px] text-xl"
        :label="e"
        :title="EMOJI_TOOLTIPS[e]"
        @click="insertEmoji(e)"
      />
    </div>
  </div>
</template>


<script>
export default {
  props: { value: String },
  data() {
    return {
      inputValue: this.value,
      emitting: true,
      emojiKeyboardVisible: false,
      emojis: ["🟢", "🔴", "⌨️", "🛠", "🔍", "✅", "❌"],
      EMOJI_TOOLTIPS: {
        "🟢": "Start • Oval",
        "🔴": "End • Oval",
        "⌨️": "Input • Parallelogram",
        "🛠": "Process • Rectangle",
        "🔍": "Decision • Diamond",
        "✅": "Yes branch",
        "❌": "No branch"
      }
    };
  },
  watch: {
    value(newValue) {
      this.emitting = false;
      this.inputValue = newValue;
      this.$nextTick(() => (this.emitting = true));
    },
    inputValue(newValue) {
      if (!this.emitting) return;
      this.$emit("update:value", newValue);
    },
  },
  methods: {
    updateValue() {
      this.inputValue = this.value;
    },
    uploadIt() {
      this.$q.notify({ message: "Server unavailable. Check connectivity.", color: "red-5", textColor: "white", icon: "warning" });
    },
    saveWork() {
      this.$emit("save", this.inputValue);
    },
    toggleEmojiKeyboard() {
      this.emojiKeyboardVisible = !this.emojiKeyboardVisible;
    },
    insertEmoji(emoji) {
      const editor = this.$refs.qRef;
      editor.focus();

      const sel = window.getSelection();
      if (!sel || sel.rangeCount === 0) {
        this.inputValue += emoji;
      } else {
        const range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(document.createTextNode(emoji));
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
        // Grab HTML from QEditor's editable div
        this.inputValue = editor.$el.querySelector('[contenteditable]').innerHTML;
      }

      // Keep v-model in sync
      this.$emit("update:value", this.inputValue);

      // Send event to Python
      this.$emit_event("emoji-inserted", emoji);
    }
  }
};
</script>
