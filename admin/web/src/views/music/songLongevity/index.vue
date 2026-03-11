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
          return await request({ url: '/api/music/song-longevity/', method: 'get', params: query })
        },
        addRequest: async (req: AddReq) => {
          return await request({ url: '/api/music/song-longevity/', method: 'post', data: req.form })
        },
        editRequest: async (req: EditReq) => {
          return await request({ url: `/api/music/song-longevity/${req.row.song_id}/`, method: 'put', data: req.form })
        },
        delRequest: async (req: DelReq) => {
          return await request({ url: `/api/music/song-longevity/${req.row.song_id}/`, method: 'delete' })
        },
      },
      columns: {
        song_id: {
          title: '歌曲ID',
          type: 'text',
          column: { width: 120 },
          form: {
            rules: [{ required: true, message: '请输入歌曲ID' }]
          }
        },
        song_name: {
          title: '歌曲名称',
          type: 'text',
          search: { show: true },
          column: { minWidth: 150 },
          form: {
            rules: [{ required: true, message: '请输入歌曲名称' }]
          }
        },
        singer_name: {
          title: '歌手',
          type: 'text',
          search: { show: true },
          column: { width: 120 },
          form: { show: true }
        },
        total_weeks: {
          title: '总留榜周数',
          type: 'number',
          column: { width: 100 },
          form: { show: true }
        },
        champion_weeks: {
          title: '夺冠周数',
          type: 'number',
          column: { width: 100 },
          form: { show: true }
        },
        history_best_rank: {
          title: '历史最好排名',
          type: 'number',
          column: { width: 120 },
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
