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
          return await request({ url: '/api/music/weekly-chart/', method: 'get', params: query })
        },
        addRequest: async (req: AddReq) => {
          return await request({ url: '/api/music/weekly-chart/', method: 'post', data: req.form })
        },
        editRequest: async (req: EditReq) => {
          return await request({ url: `/api/music/weekly-chart/${req.row.id}/`, method: 'put', data: req.form })
        },
        delRequest: async (req: DelReq) => {
          return await request({ url: `/api/music/weekly-chart/${req.row.id}/`, method: 'delete' })
        },
      },
      columns: {
        id: {
          title: 'ID',
          type: 'number',
          column: { show: false },
          form: { show: false }
        },
        issue: {
          title: '期数',
          type: 'number',
          search: { show: true },
          column: { width: 80 },
          form: {
            rules: [{ required: true, message: '请输入期数' }]
          }
        },
        rank: {
          title: '排名',
          type: 'number',
          column: { width: 70 },
          form: {
            rules: [{ required: true, message: '请输入排名' }]
          }
        },
        song_id: {
          title: '歌曲ID',
          type: 'text',
          column: { width: 100 },
          form: {
            rules: [{ required: true, message: '请输入歌曲ID' }]
          }
        },
        song_name: {
          title: '歌曲名',
          type: 'text',
          search: { show: true },
          column: { minWidth: 150 },
          form: {
            rules: [{ required: true, message: '请输入歌曲名' }]
          }
        },
        singer_id: {
          title: '歌手ID',
          type: 'text',
          column: { width: 100 },
          form: { show: true }
        },
        singer_name: {
          title: '歌手',
          type: 'text',
          search: { show: true },
          column: { width: 120 },
          form: { show: true }
        },
        uni_index: {
          title: '综合指数',
          type: 'text',
          column: { width: 100 },
          form: { show: true }
        },
        new_flag: {
          title: '新入榜',
          type: 'text',
          column: { width: 80, align: 'center' },
          form: { show: true }
        },
        cover_image: {
          title: '封面图URL',
          type: 'text',
          column: { show: false },
          form: { show: true }
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
        height: 'auto'
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
