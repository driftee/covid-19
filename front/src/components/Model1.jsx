import { Button, Card, Form, Input, Select, Slider } from "antd";
import { useEffect, useState } from "react";
import request from "umi-request";
import { useDebounce } from "use-debounce";

import * as echarts from 'echarts';

const provinces = [{k:"上海",v:"上海"},
{k:"北京",v:"北京"},
{k:"广东",v:"广东"},
{k:"江苏",v:"江苏"},
{k:"浙江",v:"浙江"},
{k:"山东",v:"山东"},
{k:"天津",v:"天津"},
{k:"重庆",v:"重庆"},
{k:"四川",v:"四川"},
{k:"河北",v:"河北"},
{k:"山西",v:"山西"},
{k:"内蒙古",v:"内蒙古"},
{k:"辽宁",v:"辽宁"},
{k:"吉林",v:"吉林"},
{k:"黑龙江",v:"黑龙江"},
{k:"安徽",v:"安徽"},
{k:"福建",v:"福建"},
{k:"江西",v:"江西"},
{k:"河南",v:"河南"},
{k:"湖南",v:"湖南"},
{k:"广西",v:"广西"},
{k:"湖北",v:"湖北"},
{k:"陕西",v:"陕西"},
{k:"新疆",v:"新疆"},
{k:"青海",v:"青海"},
{k:"宁夏",v:"宁夏"},
{k:"甘肃",v:"甘肃"},
{k:"西藏",v:"西藏"},
{k:"云南",v:"云南"},
{k:"海南",v:"海南"},
{k:"贵州",v:"贵州"},
{k:"香港",v:"香港"},
{k:"澳门",v:"澳门"},
{k:"台湾",v:"台湾"}];

const hasDataProvinces = [
    {
        name: "北京",
        key: "北京",
        value: "北京",
        params: {
            e12: 100,
            e3: 50,
            I: 350,
            Q: 1880
        }
    },
    {
        name: "深圳",
        key: "深圳",
        value: "深圳",
        params: {
            e12: 6,
            e3: 3,
            I: 21,
            Q: 1840
        }
    },
    {
        name: "香港",
        key: "香港",
        value: "香港",
        params: {
            e12: 300,
            e3: 150,
            I: 1050,
            Q: 330240
        }
    },
    {
        name: "上海",
        key: "上海",
        value: "上海",
        params: {
            e12: 40000,
            e3: 20000,
            I: 140000,
            Q: 43000
        }
    }
];

const Model1 = () => {
    
    const [form] = Form.useForm();
    const [data, setData] = useState([]);

    const [predictDays, setPredictDays] = useState(30);
    const [truePredictDays] = useDebounce(predictDays, 500);


    useEffect(() => {

        const initialValues = {
            province: "北京",
            e12: 100,
            e3: 50,
            I: 350,
            Q: 1880,
            day_to_predict: 30
        }

        form.setFieldsValue(initialValues);
        request.post("/Backend/model_api/", {data: initialValues}).then((res) => {
            // console.log(res);
            setData(res);
        });
    }, []);


    const handleSelectCity = (value) => {


        var params = hasDataProvinces.find(item => item.key == value).params;
        form.setFieldsValue(params);

        
        request.post("/Backend/model_api/", {data: {
            province: value,
            day_to_predict: form.getFieldValue("day_to_predict"),
            ...params
        }}).then((res) => {
            // console.log(res);
            setData(res);
        });

    }



    useEffect(() => {
        var chartDom = document.getElementById('figure1');
        var myChart = echarts.getInstanceByDom(chartDom);

        if (!myChart) {
            myChart = echarts.init(chartDom);
        }

        window.addEventListener('resize', () => {
            myChart.resize();
        });


        var option = {
            legend: {
              data: ['模拟的PI值','真实值', "预测的PI值"]
            },
            xAxis: {
              type: 'category',
            //   boundaryGap: false,
              scale: true,
            //   data: data.predictX,
              name: "天数"
            },
            yAxis: {
              type: 'value',
              scale: true,
                name: "" 

            },
            series: [
              {
                name: '模拟的PI值',
                type: 'line',
                // stack: 'Total',
                data: data.simpI
              },
              {
                name: '真实值',
                type: 'line',
                // stack: 'Total',
                data: data.truepI
              },
              {
                name: "预测的PI值",
                type: "line",
                data: data.predictpI?.map((item, index) => [index + data.x.length, item]),
                color: "cyan"
              }
            ]
          };

        
          myChart.setOption(option);



    }, [data]);
    useEffect(() => {




        var chartDom = document.getElementById('figure2');
        var myChart = echarts.getInstanceByDom(chartDom);

        if (!myChart) {
            myChart = echarts.init(chartDom);
        }

        window.addEventListener('resize', () => {
            myChart.resize();
        });


        var option = {
            legend: {
              data: ['模拟的Q值','真实值', "预测的Q值"]
            },

            xAxis: {
              type: 'category',
            //   boundaryGap: false,
              scale: true,
            //   data: data.x,
              name: "天数"
            },
            yAxis: {
              type: 'value',
              scale: true,
                name: "" 
                
            },
            series: [
              {
                name: '模拟的Q值',
                type: 'line',
                // stack: 'Total',
                data: data.simQ
              },
              {
                name: '真实值',
                type: 'line',
                // stack: 'Total',
                data: data.trueQ
              },
              {
                name: "预测的Q值",
                type: "line",
                data: data.predictQ?.map((item, index) => [index + data.x.length, item]),
                color: "cyan"
              }
            ]
          };

        
          myChart.setOption(option);


    }, [data]);


    useEffect(() => {


        var chartDom = document.getElementById('figure3');
        var myChart = echarts.getInstanceByDom(chartDom);

        if (!myChart) {
            myChart = echarts.init(chartDom);
        }

        window.addEventListener('resize', () => {
            myChart.resize();
        });


        var option = {
            legend: {
              data: ['rt']
            },
            // grid: {
            //   left: '3%',
            //   right: '4%',
            //   bottom: '3%',
            //   containLabel: true
            // },
            // toolbox: {
            //   feature: {
            //     saveAsImage: {}
            //   }
            // },
            xAxis: {
              type: 'category',
            //   boundaryGap: false,
              scale: true,
              data: data.x,
              name: "天数"
            },
            yAxis: {
              type: 'value',
              scale: true,
                name: "" 
                
            },
            series: [
              {
                name: 'rt',
                type: 'line',
                // stack: 'Total',
                data: data.rt
              },
            ]
          };

        
          myChart.setOption(option);




    }, [data]);



    useEffect(() => {

        var chartDom = document.getElementById('figure4');
        var myChart = echarts.getInstanceByDom(chartDom);

        if (!myChart) {
            myChart = echarts.init(chartDom);
        }

        window.addEventListener('resize', () => {
            myChart.resize();
        });


        var option = {
            legend: {
              data: ['p']
            },
            // grid: {
            //   left: '3%',
            //   right: '4%',
            //   bottom: '3%',
            //   containLabel: true
            // },
            // toolbox: {
            //   feature: {
            //     saveAsImage: {}
            //   }
            // },
            xAxis: {
              type: 'category',
            //   boundaryGap: false,
              scale: true,
              data: data.x,
              name: "天数"
            },
            yAxis: {
              type: 'value',
              scale: true,
                name: "" 
                
            },
            series: [
              {
                name: 'p',
                type: 'line',
                // stack: 'Total',
                data: data.p
              },
            ]
          };

        
          myChart.setOption(option);





    }, [data]);


    useEffect(() => {



        const params = form.getFieldsValue()

        request.post("/Backend/model_api/", {data: params}).then((res) => {
            setData(res);
        });



    }, [truePredictDays])


    const onSlide = (value) => {
        // console.log(value);

        setPredictDays(value);
    }



    return (
        <>
        <Form form={form}>

            <Form.Item label="可预测省份" name="province">
                <Select onSelect={value => handleSelectCity(value)}>
                    {hasDataProvinces.map(province => <Select.Option key={province.value} value={province.value}>{province.value}</Select.Option>)}
                </Select>
            </Form.Item>
            <Form.Item label="e12" name="e12" >
                <Input disabled ></Input>
            </Form.Item>

            <Form.Item label="e3" name="e3">
                <Input disabled></Input>
            </Form.Item> 

            <Form.Item label="I" name="I">
                <Input disabled></Input>
            </Form.Item>

            <Form.Item label="Q" name="Q">
                <Input disabled></Input>
            </Form.Item>
            <Form.Item label="预测天数" name="day_to_predict">
                <Slider min={10} max={30} onChange={onSlide}></Slider>
            </Form.Item>

{/* 
            <Form.Item>
                <Button type="primary">预测</Button>
            </Form.Item> */}
        </Form>
        <div id="figure1" style={{ width: "45%", height: "400px", display: "inline-block"}} ></div>
        <div id="figure2" style={{ width: "45%", height: "400px", display: "inline-block"}} ></div>
        <div id="figure3" style={{ width: "45%", height: "400px", display: "inline-block"}} ></div>
        <div id="figure4" style={{ width: "45%", height: "400px", display: "inline-block"}} ></div>


        
        
        
        </>
    )
}

export default Model1;