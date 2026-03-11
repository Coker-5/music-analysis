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
          return await request({ url: '/api/music/week-issue/', method: 'get', params: query })
        },
        addRequest: async (req: AddReq) => {
          return await request({ url: '/api/music/week-issue/', method: 'post', data: req.form })
        },
        editRequest: async (req: EditReq) => {
          return await request({ url: `/api/music/week-issue/${req.row.issue}/`, method: 'put', data: req.form })
        },
        delRequest: async (req: DelReq) => {
          return await request({ url: `/api/music/week-issue/${req.row.issue}/`, method: 'delete' })
        },
      },
      columns: {
        issue: {
          title: '期数编号',
          type: 'number',
          column: { width: 90 },
          form: {
            rules: [{ required: true, message: '请输入期数编号' }]
          }
        },
        title: {
          title: '标题',
          type: 'text',
          search: { show: true },
          column: { minWidth: 150 },
          form: {
            rules: [{ required: true, message: '请输入标题' }]
          }
        },
        month: {
          title: '月份',
          type: 'text',
          search: { show: true },
          column: { width: 100 },
          form: { show: true }
        },
        start_date: {
          title: '开始日期',
          type: 'date',
          column: { width: 110 },
          form: { show: true }
        },
        end_date: {
          title: '结束日期',
          type: 'date',
          column: { width: 110 },
          form: { show: true }
        },
        publish_time: {
          title: '发布时间',
          type: 'datetime',
          column: { width: 160 },
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
