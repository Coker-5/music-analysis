<template>
  <fs-page>
    <fs-crud ref="crudRef" v-bind="crudBinding" />
  </fs-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useFs, AddReq, EditReq, DelReq } from '@fast-crud/fast-crud'
import { request } from '/@/utils/service'

function createCrudOptions() {
  return {
    request: {
      pageRequest: async (query: any) => {
        const res: any = await request({ url: '/api/music/singer-stat/', method: 'get', params: query })
        return {
          currentPage: res.page,
          pageSize: res.limit,
          total: res.total,
          records: res.data
        }
      },
      addRequest: async (req: AddReq) => {
        return await request({ url: '/api/music/singer-stat/', method: 'post', data: req.form })
      },
      editRequest: async (req: EditReq) => {
        return await request({ url: `/api/music/singer-stat/${req.row.singer_id}/`, method: 'put', data: req.form })
      },
      delRequest: async (req: DelReq) => {
        return await request({ url: `/api/music/singer-stat/${req.row.singer_id}/`, method: 'delete' })
      },
    },
    columns: {
      singer_id: {
        title: '歌手ID',
        type: 'text',
        column: { width: 120 },
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
      total_count: {
        title: '总上榜次数',
        type: 'number',
        column: { width: 110 },
        form: { show: true }
      },
      champion_count: {
        title: '夺冠次数',
        type: 'number',
        column: { width: 100 },
        form: { show: true }
      },
      top3_count: {
        title: 'Top3次数',
        type: 'number',
        column: { width: 100 },
        form: { show: true }
      },
      last_updated: {
        title: '更新时间',
        type: 'datetime',
        column: { width: 160 },
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

const crudRef = ref()
const { crudBinding, crudExpose } = useFs({ createCrudOptions })
onMounted(() => {
  crudExpose.doRefresh()
})
</script>
