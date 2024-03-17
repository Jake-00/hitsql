<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { EditorView, ViewUpdate, keymap } from '@codemirror/view'
  import { Text } from "@codemirror/state"
  import { Codemirror } from 'vue-codemirror'
  import { sql } from '@codemirror/lang-sql'
  import { oneDark } from '@codemirror/theme-one-dark'
  import { acceptCompletion } from "@codemirror/autocomplete"
  import { useRequest } from 'vue-hooks-plus'
  import { postTransSQL } from './services'

  // // Set native labels' props
  // const size = ref(0.5)
  const placeHolderStr = ref('type the code...')
  const codemirrorStyle = {
    width: '100%',
    height: '100%',
    backgroundColor: '#fff',
    color: '#333'
  }
  // const buttonNames = {
  //   test: '测试代码',
  //   submit: '提交'
  // }
  
  // Set editor-related parameters and functions
  const code = ref(Text.of(['']))
  const replicatedCode = ref(Text.of(['']))
  const transpiledResult = ref('')
  function updateCode(viewUpdate: ViewUpdate) {
    code.value = viewUpdate.state.doc
    // return code
  }

  // Under setup
  // If the asynchronous function is not called in the outermost layer,
  // but inside the function, it needs to be called manually
  // function transpileSQL() {
  //   replicatedCode.value = code.value
  //   const { run, data, loading } = useRequest(() => postTransSQL(replicatedCode.value), {manual: true})
  //   run()
  //   console.log(loading)
  //   console.log(loading ? data.value?.data.output_dialect : 'no')
  //   transpiledResult.value = data.value?.data.output_sql || ''
  //   console.log(transpiledResult.value)
  // }
  const { run, data, loading } = useRequest(() => postTransSQL(code.value), {manual: true})
  // const pre_code = ref('')
  // ref(loading.value ? 'loading' : data.value?.output_sql)
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
    </div>
    <a-space>
      <a-button type="primary" shape="round" @click="run">transpile</a-button>
    </a-space>
  </a-layout-sider>
  <a-layout-content>
    <highlightjs language='sql' :code="pre_code" />
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
