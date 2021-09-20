# -*- coding: utf8 -*-
import csv
import json
import csv
import pandas as pd
from argparse import ArgumentParser
from jinja2 import Environment, PackageLoader, select_autoescape, Template
import subprocess

"""
Convert Kraken2 report to DataFrame, format it, and write it out as tsv for d3.js stacked chart.

usage:
$ python kraken2_report_formatter.py -n <samples> -f <files>
$ python kraken2_report_formatter.py -n sample1 sample2 -f ./sample1.kreport ./sample2.kreport 

"""
parser = ArgumentParser()
# -n につづけて入力するファイルをスペース区切りで指定する
parser.add_argument('-n', '--name_list', nargs='+', default=[])
parser.add_argument('-f', '--file_list', nargs='+', default=[])
args = parser.parse_args()
names = args.name_list
files = args.file_list

classification_size = 40

config = dict()
ranks = ["S", "G", "F", "O"]


def stacked_chart_formatter():
    # generate datasets for each rank
    formated_data = {}
    for r in ranks:
        # 2. sort first sample
        df0 = pd.read_table(files[0], names=("percentage", "n1", "n2", "rank", "tax_id", "name"))
        df0_by_rank = df0[df0["rank"] == r]
        d0 = df0_by_rank.sort_values(by=['percentage'], ascending=False)
        # 2.2 sort all_taxonomy by first sample
        all_taxo = [str.strip(x) for x in d0["name"].tolist()]
        all_taxo = all_taxo[0:classification_size]
        # 3 get percentage
        rows = []
        header = all_taxo.copy()
        header.insert(0, "library")
        header.append("others")
        rows.append(header)
        for i,n in enumerate(names):
            row = []
            df = pd.read_table(files[i], names=("percentage", "n1", "n2", "rank", "tax_id", "name"))
            df["name"] = df["name"].str.strip()
            dbf = df[df["rank"] == r]
            # データフレームの0:30を切り取る
            for t in all_taxo:
                d = dbf[dbf["name"] == str.strip(t)]
                # 1行のdataframeの5番目のnameカラムの値を取得
                try:
                    row.append(d.iat[0,0])
                except:
                    row.append(0)
            # 100 - リストした分類のpercentage総量をothersのpercentageとし末尾に追加
            val_others = sum(row)
            row.append(100-val_others)

            row.insert(0, n)
            row = [str(x) for x in row]
            rows.append(row)
        # write out csv

        with open('./html/rank_{}.csv'.format(r), 'w') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

        # 改行コード付きカンマ区切り文字列を追加する
        s = ""
        for row in rows:
            s = s + ",".join(row) + "\\n"

        formated_data[r] = s

    # HTMLに直接記述する場合
    # 5. htmlを生成し、ファイルを開く
    template_base = '''
    <!DOCTYPE html>
    <style>
    
        .axis .domain {
            display: none;
        }
    
        .tick text {
            font-size: 14px
        }
        body > svg > g > g:nth-child(4) > g:nth-child(1) > rect {
            fill: #777777;
        }
    
    </style>
    <svg width="960" height="850"></svg>
    <script src="https://d3js.org/d3.v4.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3-color@3"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3-interpolate@3"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3-scale-chromatic@3"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3-dsv@3"></script>
    <script>
    
        var svg = d3.select("svg"),
            margin = {top: 20, right: 250, bottom: 70, left: 40},
            width = +svg.attr("width") - margin.left - margin.right,
            height = +svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
        var x = d3.scaleBand()
            .rangeRound([0, width])
            .paddingInner(0.05)
            .align(0.1);
    
        var y = d3.scaleLinear()
            .rangeRound([height, 0]);
    
        var z = d3.scaleOrdinal()
            .range(d3.schemeTableau10);
        

        var S = "{{ data_s }}"

        var G = "{{ data_g }}"

        var F = "{{ data_f }}"

        var O = "{{ data_o }}"

        var dataset = {};
        dataset["S"] = S;
        dataset["G"] = G;
        dataset["F"] = F;
        dataset["O"] = O;
        
        function loadsamples(f) {
                var data = d3.csvParse(dataset[f], (d, _, columns) => {
                        var total = 100;
                        d.total = total;
                        return d
                });
                
                var keys = data.columns.slice(1);

                data.sort(function (a, b) {
                    return b.total - a.total;
                });
                x.domain(data.map(function (d) {
                    return d.library;
                }));
                y.domain([0, d3.max(data, function (d) {
                    return d.total;
                })]).nice();
                z.domain(keys);

                // Barplot
                g.append("g")
                    .selectAll("g")
                    .data(d3.stack().keys(keys)(data))
                    .enter().append("g")
                    .attr("fill", function (d) {
                        if (d.key == "others"){
                            return "#777777"
                        }else {
                            return z(d.key);
                        }
                    })
                    .selectAll("rect")
                    .data(function (d) {
                        return d;
                    })
                    .enter().append("rect")
                    .attr("x", function (d) {
                        return x(d.data.library);
                    })
                    .attr("y", function (d) {
                        return y(d[1]);
                    })    //  Errory: expected length, NaN
                    .attr("height", function (d) {
                        return y(d[0]) - y(d[1]);
                    })
                    .attr("width", x.bandwidth());

                g.append("g")
                    .attr("class", "axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(x).tickSize(10, 15, 10));

                g.append("g")
                    .attr("class", "axis")
                    .call(d3.axisLeft(y).ticks(null, "s"))
                    .append("text")
                    .attr("x", -35)
                    .attr("y", y(y.ticks().pop()) - 15)
                    .attr("dy", "0.32em")
                    .attr("fill", "#000")
                    .attr("font-weight", "bold")
                    .attr("text-anchor", "start")
                    .text("Population");

                // scientific name group
                var legend = g.append("g")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", 12)
                    .attr("text-anchor", "end")
                    .selectAll("g")
                    .data(keys.slice().reverse())
                    .enter().append("g")
                    .attr("transform", function (d, i) {
                        return "translate(250," + (i * 20) + ")";
                    });

                legend.append("rect")
                    .attr("x", width - 19)
                    .attr("width", 19)
                    .attr("height", 19)
                    .attr("fill", z);

                // scientific name
                legend.append("text")
                    .attr("x", width - 24)
                    .attr("y", 9.5)
                    .attr("dy", "0.32em")
                    .text(function (d) {
                        return d;
                    });

                // rank switch
                var ranks = ["S", "G", "F", "O"]
                var switches = g.append("g")
                    .attr("width", 300)
                    .attr("hight", 50)
                    .attr("class", "switch")
                    .attr("fill", "black")
                    .attr("transform", "translate(300, 820)");

                switches.selectAll("text")
                    .data(ranks)
                    .enter().append("text")
                    .text(function (d) {
                        return d
                    })
                    .attr("font-weight", function (d,i) {
                        if (d == f){return "bolder"} else {return "normal"}
                    })
                    .attr("transform", function (d, i) {
                        return "translate(" + i * 15 + ",0)";
                    })
                    .on("click", function (d) {
                        window.open("./d3.html?rank=" + d, "_self")
                    })
        }
    
        var url = new URL(window.location.href);
        var params = url.searchParams;
        var r = params.get("rank") ? params.get("rank"): "S";
        loadsamples(r)
    
    </script>
    </html>
    
    '''
    population = {}
    template = Template(template_base)
    output = template.render(data_s=formated_data["S"], data_g=formated_data["G"], data_f=formated_data["F"], data_o=formated_data["O"])
    with open("./d3.html", "w") as outh:
        outh.write(output)


stacked_chart_formatter()
subprocess.run(['open', './d3.html'])