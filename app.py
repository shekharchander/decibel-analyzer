from flask import Flask
app=Flask(__name__)
from processing import Audio
@app.route('/favicon.ico')
def nil():
    return 'not known'
@app.route('/<fileName>')
def main(fileName):
    fileName=fileName.replace('%25','%').replace("%2F","/")
    data=Audio(fileName)
    pauses=data.get_slient_parts()
    return {
    "StandardDeviation": data.standvn,
    "meandb": data.mean,
    "mediandb": data.median,
    "variation": data.variance,
    "quartile1": data.Q1,
    "quartile3": data.Q3,
    "behavior_analysis": {
        "pauses": {
            "1_sec_pause": pauses[0],
            "2_secs_pause": pauses[1],
            "3_secs_pause": pauses[2],
            "4_secs_pause": pauses[3],
            "5_secs_pause": pauses[4],
            "6_secs_pause": pauses[5],
            "more_10_secs_pause": pauses[6]
        }
    }
}
if __name__=='__main__':
    app.run()