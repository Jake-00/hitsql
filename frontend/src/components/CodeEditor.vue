<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { EditorView, ViewUpdate, keymap } from '@codemirror/view'
  import { Text } from "@codemirror/state"
  import { Codemirror } from 'vue-codemirror'
  import { sql } from '@codemirror/lang-sql'
  import { acceptCompletion } from "@codemirror/autocomplete"
  import { useRequest } from 'vue-hooks-plus'
  import { getDialectsList, postTransSQL } from './services'
  import { useClipboard } from '@vueuse/core'
  import { Message } from '@arco-design/web-vue'
  import { h } from 'vue'
  import { IconCheckCircle } from '@arco-design/web-vue/es/icon'

  const placeHolderStr = ref('type the sql...')
  const codemirrorStyle = {
    width: '100%',
    height: '100%',
    backgroundColor: '#fff',
    color: '#333'
  }
  
  // Set editor-related parameters and functions
  const code = ref(Text.of(['']))
  const replicatedCode = ref(Text.of(['']))
  const transpiledResult = ref('')
  function updateCode(viewUpdate: ViewUpdate) {
    code.value = viewUpdate.state.doc
    // return code
  }

  // Setting dialect bar
  const dialects_info = getDialectsList()
  const input_dialect = ref('hive')
  const output_dialect = ref('presto')
  function update_in_dialect(item_obj: any) {
    input_dialect.value = item_obj.value
  }
  function update_out_dialect(item_obj: any) {
    output_dialect.value = item_obj.value
  }

  const { run, data, loading } = useRequest(() => postTransSQL(code.value, input_dialect.value, output_dialect.value), {manual: true})
  const pre_code = computed(() => {
    return loading.value ? 'loading' : data.value?.output_sql || ''
  })

  // remove vue-codemirror outline when focused
  const styleTheme = EditorView.baseTheme({
    "&.cm-editor.cm-focused": {
      outline: '0'
    }
  });
  const extensions = [
    styleTheme
    // , oneDark
    , sql(), 
    // using tab to autocomplete 
    keymap.of([{key: "Tab", run: acceptCompletion}])
  ]

  // clipboard
  const source = ref('Hello')
  const { text, copy, copied, isSupported } = useClipboard({ source })
  const clip_with_msg = (pre_code: string) => {
    copy(pre_code)
    Message.info(
      {
        content:'Copied!'
        , position:'bottom'
        , icon: () => h(IconCheckCircle)
      }
    )
  }

</script>

<template>
  <a-layout-sider :resize-directions="['right']">
    <div class="editor-area">
      <codemirror 
        :autofocus=true
        :placeholder="placeHolderStr"
        :style="codemirrorStyle"
        class="code"
        @update="updateCode"
        :extensions="extensions"
      ></codemirror>
      <a-select :style="{width:'160px'}" placeholder="Select" :trigger-props="{ autoFitPopupMinWidth: true }" @change="update_in_dialect">
        <a-option v-for="dialect of dialects_info" :value="dialect" :label="dialect.label" />
      </a-select>
      <icon-arrow-right />
      <a-select :style="{width:'160px'}" placeholder="Select" :trigger-props="{ autoFitPopupMinWidth: true }" @change="update_out_dialect">
        <a-option v-for="dialect of dialects_info" :value="dialect" :label="dialect.label" />
      </a-select>
      <a-space>
        <a-button type="primary" shape="round" @click="run">transpile</a-button>
      </a-space>
    </div>
  </a-layout-sider>
  <a-layout-content>
    <highlightjs language='sql' :code="pre_code" />
    <a-space class="copy-button">
        <a-button type="primary" shape="round" @click="clip_with_msg(pre_code)">copy</a-button>
    </a-space>
  </a-layout-content>
</template>

<style>
.editor-area {
  height: 90%;
  width: 100%;
  /* overflow: hidden; */
  /* position: fixed; */
  /* background-color: aliceblue; */
}
.a-layout-content {
  white-space: pre-line;
}
.highlightjs {
  height: 100%;
}
</style>
