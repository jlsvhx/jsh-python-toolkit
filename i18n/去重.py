def generate_sql_case(text):
    lines = text.split('\n')
    statements = set()
    for line in lines:
        if line.strip():  # 忽略空行
            line = line.strip("'")
            line = line.strip()
            if line in statements:
                pass
            else:
                statements.add(line)
    my_list = sorted(list(statements))
    print("\n".join(my_list))



input_text = """
'设备A主控温度'
'设备A主控回流温度'
'设备A湿度'
'设备ACO2'
'设备A风门'
'设备A翻蛋'
'设备A主控温度'
'设备A主控回流温度'
'设备A湿度'
'设备ACO2'
'设备A风门'
'设备A翻蛋'
'设备B主控温度'
'设备B主控回流温度'
'设备B湿度'
'设备BCO2'
'设备B风门'
'设备B翻蛋'
'设备A主控温度1'
'设备A主控温度2'
'设备A主控回流温度1'
'设备A主控回流温度2'
'设备A湿度'
'设备ACO2'
'设备A风门1'
'设备A风门2'
'设备A翻蛋'
'设备B主控温度1'
'设备B主控温度2'
'设备B主控回流温度1'
'设备B主控回流温度2'
'设备B湿度'
'设备BCO2'
'设备B风门1'
'设备B风门2'
'设备B翻蛋'
'设备A主控温度'
'左入口温度'
'右入口温度'
'调温温度'
'湿度'
'设备B主控温度'
'左入口温度'
'右入口温度'
'调温温度'
'湿度'
'设备A主控温度'
'设备A湿度'
'设备ACO2'
'设备A风门'
'设备A翻蛋'
'设备B主控温度'
'设备B湿度'
'设备BCO2'
'设备B风门'
'设备B翻蛋'
'设备A主控温度1'
'设备A主控温度2'
'设备A湿度'
'设备ACO2'
'设备A风门1'
'设备A风门2'
'设备A翻蛋'
'设备B主控温度1'
'设备B主控温度2'
'设备B湿度'
'设备BCO2'
'设备B风门1'
'设备B风门2'
'设备B翻蛋'
'设备A温度'
'设备A湿度'
'设备B温度'
'设备B湿度'
'设备A室外温度采样'
'设备A送风温度采样'
'设备A送风温度设定'
'设备A静压室温度采样'
'设备A静压室温度设定'
'设备A存发苗间温度采样'
'设备A捡苗间温度采样'
'设备A存发苗间温度设定'
'设备A捡苗间温度设定'
'设备A静压室湿度采样'
'设备A静压室湿度设定'
'设备A存发苗间湿度采样'
'设备A存发苗间湿度设定'
'设备B室外温度采样'
'设备B送风温度采样'
'设备B送风温度设定'
'设备B静压室温度采样'
'设备B静压室温度设定'
'设备B存发苗间温度采样'
'设备B捡苗间温度采样'
'设备B存发苗间温度设定'
'设备B捡苗间温度设定'
'设备B静压室湿度采样'
'设备B静压室湿度设定'
'设备B存发苗间湿度采样'
'设备B存发苗间湿度设定'
'设备A室外温度采样'
'设备A送风温度采样'
'设备A送风温度设定'
'设备A静压室温度采样'
'设备A静压室温度设定'
'设备A存发苗间温度采样'
'设备A捡苗间温度采样'
'设备A存发苗间温度设定'
'设备A捡苗间温度设定'
'设备A水箱温度采样'
'设备A积水盘温度采样'
'设备A机房温度采样'
'设备A水箱孵化温度采样'
'设备A水箱温度设定'
'设备A积水盘温度设定'
'设备A机房温度设定'
'设备A水箱孵化温度设定'
'设备A静压室湿度采样'
'设备A静压室湿度设定'
'设备A存发苗间湿度采样'
'设备A存发苗间湿度设定'
'设备B室外温度采样'
'设备B送风温度采样'
'设备B送风温度设定'
'设备B静压室温度采样'
'设备B静压室温度设定'
'设备B存发苗间温度采样'
'设备B捡苗间温度采样'
'设备B存发苗间温度设定'
'设备B捡苗间温度设定'
'设备B水箱温度采样'
'设备B积水盘温度采样'
'设备B机房温度采样'
'设备B水箱孵化温度采样'
'设备B水箱温度设定'
'设备B积水盘温度设定'
'设备B机房温度设定'
'设备B水箱孵化温度设定'
'设备B静压室湿度采样'
'设备B静压室湿度设定'
'设备B存发苗间湿度采样'
'设备B存发苗间湿度设定'
'设备A冷水箱温度采样'
'设备A热水箱温度采样'
'设备A冷水箱2温度采样'
'设备A热水箱2温度采样'
'设备A水箱孵化冷水温度采样'
'设备A机房温度采样'
'设备A室外温度采样'
'设备A积水盘温度采样'
'设备A热水箱温度设定'
'设备A冷水箱温度设定'
'设备A水箱孵化冷水温度设定'
'设备A机房温度设定'
'设备A积水盘温度设定'
'设备A高温水源热泵1负荷'
'设备A高温水源热泵2负荷'
'设备A积水盘温度2'
'设备B冷水箱温度采样'
'设备B热水箱温度采样'
'设备B冷水箱2温度采样'
'设备B热水箱2温度采样'
'设备B水箱孵化冷水温度采样'
'设备B机房温度采样'
'设备B室外温度采样'
'设备B积水盘温度采样'
'设备B热水箱温度设定'
'设备B冷水箱温度设定'
'设备B水箱孵化冷水温度设定'
'设备B机房温度设定'
'设备B积水盘温度设定'
'设备B高温水源热泵1负荷'
'设备B高温水源热泵2负荷'
'设备B积水盘温度2'
'设备A静压室温度测量值'
'设备A静压室温度设定值'
'设备A静压室湿度测量值'
'设备A静压室湿度设定值'
'设备A静压室压力测量值'
'设备A静压室压力设定值'
'设备A送风温度'
'设备A送风湿度'
'设备A室外温度'
'设备A室外湿度'
'设备A排风区1压力测量值'
'设备A排风区1压力设定值'
'设备A排风区2压力测量值'
'设备A排风区2压力设定值'
'设备A排风区3压力测量值'
'设备A排风区3压力设定值'
'设备A排风区4压力测量值'
'设备A排风区4压力设定值'
'设备A送风风机风量值'
'设备A送风风机风量设定'
'设备A排风区1风机风量'
'设备A排风区1风机风量设定'
'设备A排风区2风机风量'
'设备A排风区2风机风量设定'
'设备A排风区3风机风量'
'设备A排风区3风机风量设定'
'设备A排风区4风机风量'
'设备A排风区4风机风量设定'
'设备A主三通开度'
'设备A辅三通开度 '
'设备B静压室温度测量值'
'设备B静压室温度设定值'
'设备B静压室湿度测量值'
'设备B静压室湿度设定值'
'设备B静压室压力测量值'
'设备B静压室压力设定值'
'设备B送风温度'
'设备B送风湿度'
'设备B室外温度'
'设备B室外湿度'
'设备B排风区1压力测量值'
'设备B排风区1压力设定值'
'设备B排风区2压力测量值'
'设备B排风区2压力设定值'
'设备B排风区3压力测量值'
'设备B排风区3压力设定值'
'设备B排风区4压力测量值'
'设备B排风区4压力设定值'
'设备B送风风机风量值'
'设备B送风风机风量设定'
'设备B排风区1风机风量'
'设备B排风区1风机风量设定'
'设备B排风区2风机风量'
'设备B排风区2风机风量设定'
'设备B排风区3风机风量'
'设备B排风区3风机风量设定'
'设备B排风区4风机风量'
'设备B排风区4风机风量设定'
'设备B主三通开度'
'设备B辅三通开度 '
'设备A存发苗/处理间温度测量值'
'设备A存发苗/处理间温度设定值'
'设备A存发苗/处理间湿度测量值'
'设备A存发苗/处理间湿度设定值'
'设备A存发苗/处理间CO2测量值'
'设备A存发苗/处理间CO2设定值'
'设备A送风温度'
'设备A送风湿度'
'设备A室外温度'
'设备A室外湿度'
'设备A存发苗/处理间压力测量值'
'设备A存发苗/处理间压力设定值'
'设备A捡苗间压力测量值'
'设备A捡苗间压力设定值'
'设备A捡苗间温度'
'设备A捡苗间湿度'
'设备A送风风机风量'
'设备A送风风机风量设定'
'设备A存发苗/处理间排风风机风量'
'设备A存发苗/处理间排风风机风量设定'
'设备A捡苗间排风风机风量'
'设备A捡苗间排风风机风量设定'
'设备A主三通开度'
'设备A辅三通开度'
'设备B存发苗/处理间温度测量值'
'设备B存发苗/处理间温度设定值'
'设备B存发苗/处理间湿度测量值'
'设备B存发苗/处理间湿度设定值'
'设备B存发苗/处理间CO2测量值'
'设备B存发苗/处理间CO2设定值'
'设备B送风温度'
'设备B送风湿度'
'设备B室外温度'
'设备B室外湿度'
'设备B存发苗/处理间压力测量值'
'设备B存发苗/处理间压力设定值'
'设备B捡苗间压力测量值'
'设备B捡苗间压力设定值'
'设备B捡苗间温度'
'设备B捡苗间湿度'
'设备B送风风机风量'
'设备B送风风机风量设定'
'设备B存发苗/处理间排风风机风量'
'设备B存发苗/处理间排风风机风量设定'
'设备B捡苗间排风风机风量'
'设备B捡苗间排风风机风量设定'
'设备B主三通开度'
'设备B辅三通开度'
"""

generate_sql_case(input_text)