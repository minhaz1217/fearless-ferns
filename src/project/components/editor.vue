<!-- Based on https://quasar.dev/vue-components/editor#example--add-new-commands -->
<template>
  <q-editor
    ref="qRef"
    v-bind="$attrs"
    v-model="inputValue"
    :definitions="{
      save: {
        tip: 'Save your work',
        icon: 'save',
        label: 'Save',
        handler: saveWork,
      },
      upload: {
        tip: 'Upload to cloud',
        icon: 'cloud_upload',
        label: 'Upload',
        handler: uploadIt,
      },
    }"
    :toolbar="[
      ['bold', 'italic', 'strike', 'underline'],
      ['upload', 'save'],
    ]"
  >
    <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
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
  },
};
</script>
