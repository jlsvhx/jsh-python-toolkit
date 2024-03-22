import { listMachinedatanewdqdxt } from '@/api/history/machinedatanewdqdxt'
import { listMachinedatanewsqdxt } from '@/api/history/machinedatanewsqdxt'
import { listMachinedatanewxdhl } from '@/api/history/machinedatanewxdhl'
import { listMachinedatanew576 } from '@/api/history/machinedatanew576'
import { listMachinedatanew1152 } from '@/api/history/machinedatanew1152'
import { listAirconditionerdata } from '@/api/history/airconditionerdata'
import { listSldata } from '@/api/history/sldata'
import { listQrhsdata } from '@/api/history/qrhsdata'
import { listTblfunctionroom } from '@/api/history/tblfunctionroom'
import { listTblnewairmaindata } from '@/api/history/tblnewairmaindata'
import { listTblnewairreardata } from '@/api/history/tblnewairreardata'
import {
  CO2_YAXIS,
  FREQ_YAXIS,
  HUMI_YAXIS,
  PRESS_YAXIS,
  TEMP_YAXIS,
  TURN_YAXIS,
  VALVE_YAXIS
} from '@/enum/history/yAxis'
import { KT_Alarm, NEW_1152, NEW_576, NEW_DQDXT, NEW_SQDXT, NEW_XDHL, QRHS_Alarm, SL_Alarm } from '@/static/config'
import i18n from "@/lang";
export const HISTORY = {
  12: {
    exportURL: '/history/machinedatanewdqdxt/export',
    locationType: 12,
    showHatchDay: true,
    showHatchHour: true,
    englishLabel: ['maintemp', 'returntemp', 'humi', 'co2', 'valve', 'turncount'],
    // A_legendData: ['设备A主控温度', '设备A主控回流温度', '设备A湿度', '设备ACO2', '设备A风门', '设备A翻蛋'],
    A_legendData: ['设备A主控温度', '设备A主控回流温度', '设备A湿度', '设备ACO2', '设备A风门', '设备A翻蛋'],
    B_legendData: ['设备B主控温度', '设备B主控回流温度', '设备B湿度', '设备BCO2', '设备B风门', '设备B翻蛋'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS, CO2_YAXIS, VALVE_YAXIS, TURN_YAXIS],
    yAxisMap: [0, 0, 1, 2, 3, 4],
    alarm: NEW_DQDXT,
    // alarm: this.$t('NEW_DQDXT'),
    getHistory: (queryParams) => {
      return listMachinedatanewdqdxt(queryParams)
    }
  },
  17: {
    exportURL: '/history/machinedatanewsqdxt/export',
    locationType: 17,
    showHatchDay: true,
    showHatchHour: true,
    englishLabel: ['maintemp1', 'maintemp2', 'returntemp1', 'returntemp2', 'humi', 'co2', 'valve1', 'valve2', 'turncount'],
    A_legendData: ['设备A主控温度1', '设备A主控温度2', '设备A主控回流温度1', '设备A主控回流温度2', '设备A湿度', '设备ACO2', '设备A风门1', '设备A风门2', '设备A翻蛋'],
    B_legendData: ['设备B主控温度1', '设备B主控温度2', '设备B主控回流温度1', '设备B主控回流温度2', '设备B湿度', '设备BCO2', '设备B风门1', '设备B风门2', '设备B翻蛋'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS, CO2_YAXIS, VALVE_YAXIS, TURN_YAXIS],
    yAxisMap: [0, 0, 0, 0, 1, 2, 3, 3, 4],
    alarm: NEW_SQDXT,
    getHistory: (queryParams) => {
      return listMachinedatanewsqdxt(queryParams)
    }
  },
  18: {
    exportURL: '/history/machinedatanewxdhl/export',
    locationType: 18,
    showHatchDay: true,
    showHatchHour: true,
    englishLabel: ['maintemp', 'lefttemp', 'righttemp', 'aitemp', 'humi'],
    A_legendData: ['设备A主控温度', '左入口温度', '右入口温度', '调温温度', '湿度'],
    B_legendData: ['设备B主控温度', '左入口温度', '右入口温度', '调温温度', '湿度'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS],
    alarm: NEW_XDHL,
    yAxisMap: [0, 0, 0, 0, 1],
    getHistory: (queryParams) => {
      return listMachinedatanewxdhl(queryParams)
    }
  },
  20: {
    exportURL: '/history/machinedatanew576/export',
    locationType: 20,
    showHatchDay: true,
    showHatchHour: true,
    englishLabel: ['maintemp', 'humi', 'co2', 'valve', 'turncount'],
    A_legendData: ['设备A主控温度', '设备A湿度', '设备ACO2', '设备A风门', '设备A翻蛋'],
    B_legendta: ['设备B主控温度', '设备B湿度', '设备BCO2', '设备B风门', '设备B翻蛋'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS, CO2_YAXIS, VALVE_YAXIS, TURN_YAXIS],
    yAxisMap: [0, 1, 2, 3, 4],
    alarm: NEW_576,
    getHistory: (queryParams) => {
      return listMachinedatanew576(queryParams)
    }
  },
  21: {
    exportURL: '/history/machinedatanew1152/export',
    locationType: 21,
    showHatchDay: true,
    showHatchHour: true,
    englishLabel: ['maintemp1', 'maintemp2', 'humi', 'co2', 'valve1', 'valve2', 'turncount'],
    A_legendData: ['设备A主控温度1', '设备A主控温度2', '设备A湿度', '设备ACO2', '设备A风门1', '设备A风门2', '设备A翻蛋'],
    B_legendData: ['设备B主控温度1', '设备B主控温度2', '设备B湿度', '设备BCO2', '设备B风门1', '设备B风门2', '设备B翻蛋'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS, CO2_YAXIS, VALVE_YAXIS, TURN_YAXIS],
    yAxisMap: [0, 0, 1, 2, 3, 3, 4],
    alarm: NEW_1152,
    getHistory: (queryParams) => {
      return listMachinedatanew1152(queryParams)
    }
  },
  31: {
    exportURL: '/history/tblfunctionroom/export',
    locationType: 31,
    showHatchDay: false,
    showHatchHour: false,
    englishLabel: ['temp', 'humi'],
    A_legendData: ['设备A温度', '设备A湿度'],
    B_legendData: ['设备B温度', '设备B湿度'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS],
    alarm: {},
    yAxisMap: [0, 1],
    getHistory: (queryParams) => {
      return listTblfunctionroom(queryParams)
    }
  },
  32: {
    exportURL: '/history/airconditionerdata/export',
    locationType: 32,
    showHatchDay: false,
    showHatchHour: false,
    englishLabel: ['ambienttemp', 'ventilatetemp', 'ventilatetempset', 'srtemp', 'srtempset', 'sprtemp', 'prtemp', 'sprtempset', 'prtempset', 'srhumidity', 'srhumidityset', 'sprhumidity', 'sprhumidityset'],
    A_legendData: ['设备A室外温度采样', '设备A送风温度采样', '设备A送风温度设定', '设备A静压室温度采样', '设备A静压室温度设定', '设备A存发苗间温度采样', '设备A捡苗间温度采样', '设备A存发苗间温度设定', '设备A捡苗间温度设定', '设备A静压室湿度采样', '设备A静压室湿度设定', '设备A存发苗间湿度采样', '设备A存发苗间湿度设定'],
    B_legendData: ['设备B室外温度采样', '设备B送风温度采样', '设备B送风温度设定', '设备B静压室温度采样', '设备B静压室温度设定', '设备B存发苗间温度采样', '设备B捡苗间温度采样', '设备B存发苗间温度设定', '设备B捡苗间温度设定', '设备B静压室湿度采样', '设备B静压室湿度设定', '设备B存发苗间湿度采样', '设备B存发苗间湿度设定'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS],
    yAxisMap: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    alarm: KT_Alarm,
    getHistory: (queryParams) => {
      return listAirconditionerdata(queryParams)
    }
  },
  33: {
    exportURL: '/history/sldata/export',
    locationType: 33,
    showHatchDay: false,
    showHatchHour: false,
    englishLabel: ['ambienttemp', 'ventilatetemp', 'ventilatetempset', 'srtemp', 'srtempset', 'sprtemp', 'prtemp', 'sprtempset', 'prtempset', 'watertanktemp', 'watertraytemp', 'machineroomtemp', 'watertankincubtemp', 'watertanktempset', 'watertraytempset', 'machineroomtempset', 'watertankincubtempset', 'srhumidity', 'srhumidityset', 'sprhumidity', 'sprhumidityset'],
    A_legendData: ['设备A室外温度采样', '设备A送风温度采样', '设备A送风温度设定', '设备A静压室温度采样', '设备A静压室温度设定', '设备A存发苗间温度采样', '设备A捡苗间温度采样', '设备A存发苗间温度设定', '设备A捡苗间温度设定', '设备A水箱温度采样', '设备A积水盘温度采样', '设备A机房温度采样', '设备A水箱孵化温度采样', '设备A水箱温度设定', '设备A积水盘温度设定', '设备A机房温度设定', '设备A水箱孵化温度设定', '设备A静压室湿度采样', '设备A静压室湿度设定', '设备A存发苗间湿度采样', '设备A存发苗间湿度设定'],
    B_legendData: ['设备B室外温度采样', '设备B送风温度采样', '设备B送风温度设定', '设备B静压室温度采样', '设备B静压室温度设定', '设备B存发苗间温度采样', '设备B捡苗间温度采样', '设备B存发苗间温度设定', '设备B捡苗间温度设定', '设备B水箱温度采样', '设备B积水盘温度采样', '设备B机房温度采样', '设备B水箱孵化温度采样', '设备B水箱温度设定', '设备B积水盘温度设定', '设备B机房温度设定', '设备B水箱孵化温度设定', '设备B静压室湿度采样', '设备B静压室湿度设定', '设备B存发苗间湿度采样', '设备B存发苗间湿度设定'],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS],
    yAxisMap: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    alarm: SL_Alarm,
    getHistory: (queryParams) => {
      return listSldata(queryParams)
    }
  },
  34: {
    exportURL: '/history/qrhsdata/export',
    locationType: 34,
    showHatchDay: false,
    showHatchHour: false,
    englishLabel: ['coldtanktemp', 'hottanktemp', 'coldtank2temp', 'hottank2temp', 'tankcoldtemp', 'roomtemp', 'outtemp', 'pantemp', 'tankhottempset', 'tankcoldtempset', 'tankincubcoldtempset', 'roomtempset', 'sumptempset', 'hightempwatersourceload1', 'hightempwatersourceload2', 'sumptemp2'],
    A_legendData: ['设备A冷水箱温度采样', '设备A热水箱温度采样', '设备A冷水箱2温度采样', '设备A热水箱2温度采样', '设备A水箱孵化冷水温度采样', '设备A机房温度采样', '设备A室外温度采样', '设备A积水盘温度采样', '设备A热水箱温度设定', '设备A冷水箱温度设定', '设备A水箱孵化冷水温度设定', '设备A机房温度设定', '设备A积水盘温度设定', '设备A高温水源热泵1负荷', '设备A高温水源热泵2负荷', '设备A积水盘温度2'],
    B_legendData: ['设备B冷水箱温度采样', '设备B热水箱温度采样', '设备B冷水箱2温度采样', '设备B热水箱2温度采样', '设备B水箱孵化冷水温度采样', '设备B机房温度采样', '设备B室外温度采样', '设备B积水盘温度采样', '设备B热水箱温度设定', '设备B冷水箱温度设定', '设备B水箱孵化冷水温度设定', '设备B机房温度设定', '设备B积水盘温度设定', '设备B高温水源热泵1负荷', '设备B高温水源热泵2负荷', '设备B积水盘温度2'],
    yAxis: [TEMP_YAXIS],
    alarm: QRHS_Alarm,
    yAxisMap: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    getHistory: (queryParams) => {
      return listQrhsdata(queryParams)
    }
  },
  35: {
    exportURL: '/history/tblnewairmaindata/export',
    locationType: 35,
    showHatchDay: false,
    showHatchHour: false,
    englishLabel: [
      'plenumtemp',
      'plenumtempsv',
      'plenumhumi',
      'plenumhumisv',
      'plenumpress',
      'plenumpresssv',
      'supplyairtemp',
      'supplyairhumi',
      'outdoortemp',
      'outdoorhumi',
      'exhaustpress1',
      'exhaustpresssv1',
      'exhaustpress2',
      'exhaustpresssv2',
      'exhaustpress3',
      'exhaustpresssv3',
      'exhaustpress4',
      'exhaustpresssv4',
      'supplyairfreq',
      'supplyairfreqsv',
      'exhaustfreq1',
      'exhaustfreqsv1',
      'exhaustfreq2',
      'exhaustfreqsv2',
      'exhaustfreq3',
      'exhaustfreqsv3',
      'exhaustfreq4',
      'exhaustfreqsv4',
      'mainvalveopening',
      'assistvalveopening'
    ],
    A_legendData: [
      '设备A静压室温度测量值',
      '设备A静压室温度设定值',
      '设备A静压室湿度测量值',
      '设备A静压室湿度设定值',
      '设备A静压室压力测量值',
      '设备A静压室压力设定值',
      '设备A送风温度',
      '设备A送风湿度',
      '设备A室外温度',
      '设备A室外湿度',
      '设备A排风区1压力测量值',
      '设备A排风区1压力设定值',
      '设备A排风区2压力测量值',
      '设备A排风区2压力设定值',
      '设备A排风区3压力测量值',
      '设备A排风区3压力设定值',
      '设备A排风区4压力测量值',
      '设备A排风区4压力设定值',
      '设备A送风风机风量值',
      '设备A送风风机风量设定',
      '设备A排风区1风机风量',
      '设备A排风区1风机风量设定',
      '设备A排风区2风机风量',
      '设备A排风区2风机风量设定',
      '设备A排风区3风机风量',
      '设备A排风区3风机风量设定',
      '设备A排风区4风机风量',
      '设备A排风区4风机风量设定',
      '设备A主三通开度',
      '设备A辅三通开度'
    ],
    B_legendData: [
      '设备B静压室温度测量值',
      '设备B静压室温度设定值',
      '设备B静压室湿度测量值',
      '设备B静压室湿度设定值',
      '设备B静压室压力测量值',
      '设备B静压室压力设定值',
      '设备B送风温度',
      '设备B送风湿度',
      '设备B室外温度',
      '设备B室外湿度',
      '设备B排风区1压力测量值',
      '设备B排风区1压力设定值',
      '设备B排风区2压力测量值',
      '设备B排风区2压力设定值',
      '设备B排风区3压力测量值',
      '设备B排风区3压力设定值',
      '设备B排风区4压力测量值',
      '设备B排风区4压力设定值',
      '设备B送风风机风量值',
      '设备B送风风机风量设定',
      '设备B排风区1风机风量',
      '设备B排风区1风机风量设定',
      '设备B排风区2风机风量',
      '设备B排风区2风机风量设定',
      '设备B排风区3风机风量',
      '设备B排风区3风机风量设定',
      '设备B排风区4风机风量',
      '设备B排风区4风机风量设定',
      '设备B主三通开度',
      '设备B辅三通开度'
    ],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS, PRESS_YAXIS, FREQ_YAXIS],
    yAxisMap: [0, 0, 1, 1, 2, 2, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1],
    alarm: {},
    getHistory: (queryParams) => {
      return listTblnewairmaindata(queryParams)
    }

  },
  36: {
    exportURL: '/history/tblnewairreardata/export',
    locationType: 36,
    showHatchDay: false,
    showHatchHour: false,
    englishLabel: [
      'seedlingroomtemp',
      'seedlingroomtempsv',
      'seedlingroomhumi',
      'seedlingroomhumisv',
      'seedlingroomco2',
      'seedlingroomco2sv',
      'supplyairtemp',
      'supplyairhumi',
      'outsidetemp',
      'outsidehumi',
      'seedlingroompress',
      'seedlingroompresssv',
      'pickingroompress',
      'pickingroompresssv',
      'pickingroomtemp',
      'pickingroomhumi',
      'supplyairfreq',
      'supplyairfreqsv',
      'seedlingroomexhaustfreq',
      'seedlingroomexhaustfreqsv',
      'pickingroomexhaustfreq',
      'pickingroomexhaustfreqsv',
      'mainvalveopening',
      'auxivalveopening '
    ],
    A_legendData: [
      '设备A存发苗/处理间温度测量值',
      '设备A存发苗/处理间温度设定值',
      '设备A存发苗/处理间湿度测量值',
      '设备A存发苗/处理间湿度设定值',
      '设备A存发苗/处理间CO2测量值',
      '设备A存发苗/处理间CO2设定值',
      '设备A送风温度',
      '设备A送风湿度',
      '设备A室外温度',
      '设备A室外湿度',
      '设备A存发苗/处理间压力测量值',
      '设备A存发苗/处理间压力设定值',
      '设备A捡苗间压力测量值',
      '设备A捡苗间压力设定值',
      '设备A捡苗间温度',
      '设备A捡苗间湿度',
      '设备A送风风机风量',
      '设备A送风风机风量设定',
      '设备A存发苗/处理间排风风机风量',
      '设备A存发苗/处理间排风风机风量设定',
      '设备A捡苗间排风风机风量',
      '设备A捡苗间排风风机风量设定',
      '设备A主三通开度',
      '设备A辅三通开度'
    ],
    B_legendData: [
      '设备B存发苗/处理间温度测量值',
      '设备B存发苗/处理间温度设定值',
      '设备B存发苗/处理间湿度测量值',
      '设备B存发苗/处理间湿度设定值',
      '设备B存发苗/处理间CO2测量值',
      '设备B存发苗/处理间CO2设定值',
      '设备B送风温度',
      '设备B送风湿度',
      '设备B室外温度',
      '设备B室外湿度',
      '设备B存发苗/处理间压力测量值',
      '设备B存发苗/处理间压力设定值',
      '设备B捡苗间压力测量值',
      '设备B捡苗间压力设定值',
      '设备B捡苗间温度',
      '设备B捡苗间湿度',
      '设备B送风风机风量',
      '设备B送风风机风量设定',
      '设备B存发苗/处理间排风风机风量',
      '设备B存发苗/处理间排风风机风量设定',
      '设备B捡苗间排风风机风量',
      '设备B捡苗间排风风机风量设定',
      '设备B主三通开度',
      '设备B辅三通开度'
    ],
    yAxis: [TEMP_YAXIS, HUMI_YAXIS, CO2_YAXIS, PRESS_YAXIS, FREQ_YAXIS],
    yAxisMap: [0, 0, 1, 1, 2, 2, 0, 1, 0, 1, 3, 3, 3, 3, 0, 1, 4, 4, 4, 4, 4, 4, 1, 1],
    alarm: {},
    getHistory: (queryParams) => {
      return listTblnewairreardata(queryParams)
    }
  }

}
