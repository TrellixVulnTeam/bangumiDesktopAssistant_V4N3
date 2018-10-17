import datetime,json,time
from PIL import Image

class PerChapterInfo:
    def __init__(self, bangumiTitle, updateTime: datetime.datetime, chapterId,headImg:str, chapterName="", title=""):
        self.bangumiTitle = bangumiTitle
        self.updateTime = updateTime
        self.updateTimeText = self.updateTime.strftime("%Y-%m-%d %H:%M:%S")
        self.chapterId = chapterId
        self.chapterName = chapterName
        self.title = title if title else "无"
        self.headImg = headImg

    def __str__(self):
        return json.dumps({
            "bangumiTitle": self.bangumiTitle,
            "updateTime": self.updateTimeText,
            "chapterId": self.chapterId,
            "chapterName": self.chapterName,
            "title": self.title,
            "headImg":self.headImg
        },ensure_ascii=False)

    @staticmethod
    def fromSource(source):
        if type(source) == str:
            source = json.load(source)
        updateTime = datetime.datetime.strptime(source["updateTime"], "%Y-%m-%d %H:%M:%S")
        return PerChapterInfo(bangumiTitle=source["bangumiTitle"], updateTime=updateTime,chapterId=source["chapterId"],chapterName=source["chapterName"],headImg=source["headImg"],title=source["title"])


class BangumiChapters:
    def __init__(self, info):
        self.info = info
        self.title = info["title"]

        img = Image.open(info["headImgSrc"])
        img = img.convert("RGB")
        img = img.resize((64, 64),Image.ANTIALIAS)
        imgFileName = f"{int(time.time())}.jpg"
        imgFilePath = f"../src/img/bangumiheadimg/{imgFileName}"
        img.save(imgFilePath)

        self.headImgSrc = imgFileName
        self.startChapter = info["startChapter"]

        self.startDate = info["startDate"]
        self.finishDate = info["finishDate"]

        self.updateType = info["updateType"]
        self.updateDay = info["updateDay"]
        self.updateTime = info["updateTime"]

        self.platFormTargetUrls = info["platFormTargetUrls"]

        self.follow = info["follow"]

        self.startUpdateDateTime = datetime.datetime.strptime(f"{self.startDate} {self.updateTime}:00",
                                                              "%Y-%m-%d %H:%M:%S")
        self.finalUpdateDateTime = datetime.datetime.strptime(f"{self.finishDate} {self.updateTime}:00",
                                                              "%Y-%m-%d %H:%M:%S")
        self.chapters = []
        self.makeChapters()

    def makeChapters(self):
        self.chapters = []
        if self.updateType == "weekly":
            interval = datetime.timedelta(days=7)
            updateDateTime = self.startUpdateDateTime
            chaptersCount = 0
            while self.finalUpdateDateTime >= updateDateTime >= self.startUpdateDateTime and chaptersCount <= 100:
                chaptersCount += 1
                updateDateTime += interval
                chapterId = self.startChapter + chaptersCount
                perchapterInfo = PerChapterInfo(bangumiTitle=self.title, updateTime=updateDateTime, chapterId=chapterId,
                                                chapterName=f"第{chapterId}话",headImg=self.headImgSrc, title="")
                self.chapters.append(perchapterInfo)

        elif self.updateType == "monthly":
            updateDateTime = self.startUpdateDateTime

            chaptersCount = 0
            while self.finalUpdateDateTime >= updateDateTime >= self.startUpdateDateTime and chaptersCount <= 100:
                chaptersCount += 1
                updateTimeArr = updateDateTime.strftime("%Y-%m-%d %H:%M:%S").split("-")
                m = int(updateTimeArr[1])
                if not m == 12:
                    updateTimeArr[1] = str(m + 1)
                else:
                    updateTimeArr[0] = str(int(updateTimeArr[0]) + 1)
                    updateTimeArr[1] = "1"
                updateDateTimeStr = "-".join(updateTimeArr)
                updateDateTime = datetime.datetime.strptime(updateDateTimeStr, "%Y-%m-%d %H:%M:%S")
                chapterId = self.startChapter + chaptersCount
                perchapterInfo = PerChapterInfo(bangumiTitle=self.title, updateTime=updateDateTime, chapterId=chapterId,
                                                chapterName=f"第{chapterId}话",headImg=self.headImgSrc, title="")
                self.chapters.append(perchapterInfo)
