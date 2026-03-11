<template>
  <fs-page>
    <fs-crud ref="crudRef" v-bind="crudBinding" />
  </fs-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useFs, AddReq, EditReq, DelReq, CreateCrudOptionsProps, CreateCrudOptionsRet } from '@fast-crud/fast-crud'
import { request } from '/@/utils/service'

function createCrudOptions({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
  return {
    crudOptions: {
      request: {
        pageRequest: async (query: any) => {
          return await request({ url: '/api/music/singer/', method: 'get', params: query })
        },
        addRequest: async (req: AddReq) => {
          return await request({ url: '/api/music/singer/', method: 'post', data: req.form })
        },
        editRequest: async (req: EditReq) => {
          return await request({ url: `/api/music/singer/${req.row.singer_id}/`, method: 'put', data: req.form })
        },
        delRequest: async (req: DelReq) => {
          return await request({ url: `/api/music/singer/${req.row.singer_id}/`, method: 'delete' })
        },
      },
      columns: {
        singer_id: {
          title: '歌手ID',
          type: 'text',
          column: { width: 150 },
          form: {
            rules: [{ required: true, message: '请输入歌手ID' }]
          }
        },
        singer_name: {
          title: '歌手名称',
          type: 'text',
          search: { show: true },
          column: { minWidth: 150 },
          form: {
            rules: [{ required: true, message: '请输入歌手名称' }]
          }
        },
        created_at: {
          title: '创建时间',
          type: 'datetime',
          column: { width: 180 },
          form: { show: false }
        }
      },
      toolbar: {
        buttons: {
          search: { show: true },
          add: { show: true }
        }
      },
      rowHandle: {
        edit: { show: true },
        remove: { show: true }
      },
      table: {
        striped: true,
        height: 'auto',
        scroll: { y: 500 }
      },
      pagination: {
        pageSize: 20
      }
    }
  }
}

const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions })
onMounted(() => {
  crudExpose.doRefresh()
})
</script>
