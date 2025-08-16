<!-- https://quasar.dev/vue-components/editor#example--kitchen-sink -->
<template>
  <q-editor
    ref="editor"
    v-bind="$attrs"
    v-model="inputValue"
    :definitions="{
      save: {
        tip: 'Save your work',
        icon: 'save',
        // label: 'Save',
        handler: saveWork,
      },
      upload: {
        tip: 'Upload to cloud',
        icon: 'cloud_upload',
        // label: 'Upload',
        handler: uploadIt,
      },
      emoji: {
        tip: 'Toggle Emoji Keyboard',
        icon: 'add_reaction',
        handler: toggleKeyboard,
      },
    }"
    :toolbar="[
      [
        {
          label: $q.lang.editor.align,
          icon: $q.iconSet.editor.align,
          fixedLabel: true,
          list: 'only-icons',
          options: ['left', 'center', 'right', 'justify'],
        },
        {
          label: $q.lang.editor.align,
          icon: $q.iconSet.editor.align,
          fixedLabel: true,
          options: ['left', 'center', 'right', 'justify'],
        },
      ],
      ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
      ['token', 'hr', 'link'],
      ['print', 'fullscreen', 'emoji'],
      [
        {
          label: $q.lang.editor.formatting,
          icon: $q.iconSet.editor.formatting,
          list: 'no-icons',
          options: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code'],
        },
        {
          label: $q.lang.editor.fontSize,
          icon: $q.iconSet.editor.fontSize,
          fixedLabel: true,
          fixedIcon: true,
          list: 'no-icons',
          options: [
            'size-1',
            'size-2',
            'size-3',
            'size-4',
            'size-5',
            'size-6',
            'size-7',
          ],
        },
        {
          label: $q.lang.editor.defaultFont,
          icon: $q.iconSet.editor.font,
          fixedIcon: true,
          list: 'no-icons',
          options: [
            'default_font',
            'arial',
            'arial_black',
            'comic_sans',
            'courier_new',
            'impact',
            'lucida_grande',
            'times_new_roman',
            'verdana',
          ],
        },
        'removeFormat',
      ],
      ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
      ['undo', 'redo'],
      ['viewsource', 'upload', 'save'],
    ]"
    :fonts="{
      arial: 'Arial',
      arial_black: 'Arial Black',
      comic_sans: 'Comic Sans MS',
      courier_new: 'Courier New',
      impact: 'Impact',
      lucida_grande: 'Lucida Grande',
      times_new_roman: 'Times New Roman',
      verdana: 'Verdana',
    }"
  >
    <template v-for="(_, slot) of $slots" v-slot:[slot]="slotProps">
      <slot :name="slot" v-bind="slotProps || {}" />
    </template>
  </q-editor>
</template>

<script>
export default {
  props: {
    value: String,
  },
  data() {
    return {
      inputValue: this.value,
      emitting: true,
      keyboardActive: false,
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
      this.$q.notify({
        message: "Server unavailable. Check connectivity.",
        color: "red-5",
        textColor: "white",
        icon: "warning",
      });
    },
    saveWork() {
      this.$emit("save", this.inputValue);
    },
    toggleKeyboard() {
      this.keyboardActive = !this.keyboardActive;
      this.$emit("toggle:keyboard", this.keyboardActive);
    },
    insertTextAtCursor(text) {
      const editorRef = this.$refs.editor;
      if (editorRef && editorRef.runCmd) {
        editorRef.runCmd("insertText", text);
      }
    },
  },
};
</script>
