import { Box, Button, Container, Typography } from "@mui/material";
import { useEffect, useRef, useState, useCallback } from "react";

// 時刻とその時刻における解析結果
interface TimeLine {
    // timeはhh:mm:ss形式の文字列
    time: string;
    result: "kill" | "death" | "start" | "finish";
}

// 解析結果のリスト
const initialTimeLines: TimeLine[] = [
    { time: "00:00:00", result: "start" },
    { time: "00:00:10", result: "death" },
    { time: "00:00:20", result: "kill" },
    { time: "00:00:30", result: "kill" },
    { time: "00:00:40", result: "kill" },
    { time: "00:00:50", result: "death" },
    { time: "00:01:00", result: "kill" },
    { time: "00:01:10", result: "kill" },
    { time: "00:01:20", result: "death" },
    { time: "00:01:30", result: "kill" },
    { time: "00:01:40", result: "kill" },
    { time: "00:01:50", result: "death" },
    { time: "00:02:00", result: "kill" },
    { time: "00:02:10", result: "death" },
    { time: "00:02:20", result: "kill" },
    { time: "00:02:30", result: "death" },
    { time: "00:02:40", result: "kill" },
    { time: "00:02:50", result: "death" },
    { time: "00:03:00", result: "kill" },
    { time: "00:03:10", result: "kill" },
    { time: "00:03:20", result: "death" },
    { time: "00:03:30", result: "kill" },
    { time: "00:03:40", result: "death" },
    { time: "00:03:50", result: "kill" },
    { time: "00:04:00", result: "death" },
    { time: "00:04:10", result: "kill" },
    { time: "00:04:20", result: "kill" },
    { time: "00:04:30", result: "death" },
    { time: "00:04:40", result: "kill" },
    { time: "00:04:50", result: "kill" },
    { time: "00:05:00", result: "finish" },
];

export default function App(): JSX.Element {
    const [timeLines, setTimeLines] = useState<TimeLine[]>([]);
    const [videoPath, setVideoPath] = useState<string>("");
    const videoRef = useRef<HTMLVideoElement>(null);
    const timelineRefs = useRef<(HTMLDivElement | HTMLSpanElement | null)[]>([]);

    useEffect(() => {
        setTimeLines(initialTimeLines);
    }, []);

    const handleTimeClick = useCallback(
        (time: string) => {
            if (videoRef.current) {
                const [hours, minutes, seconds] = time.split(":").map(Number);
                const secondsToJump = hours * 3600 + minutes * 60 + seconds;
                videoRef.current.currentTime = secondsToJump;
                videoRef.current.play();
            }
        },
        [videoRef]
    );

    useEffect(() => {
        const videoElement = videoRef.current;

        const handleTimeUpdate = () => {
            if (videoElement) {
                const currentTime = videoElement.currentTime;

                const closestIndex = timeLines.findIndex((timeLine) => {
                    const [hours, minutes, seconds] = timeLine.time
                        .split(":")
                        .map(Number);
                    const timeInSeconds = hours * 3600 + minutes * 60 + seconds;
                    return timeInSeconds >= currentTime;
                });

                if (closestIndex !== -1 && timelineRefs.current[closestIndex]) {
                    timelineRefs.current[closestIndex]?.scrollIntoView({
                        behavior: "smooth",
                        block: "center",
                    });
                }
            }
        };

        videoElement?.addEventListener("timeupdate", handleTimeUpdate);

        return () => {
            videoElement?.removeEventListener("timeupdate", handleTimeUpdate);
        };
    }, [timeLines]);

    // CSV形式に変換する関数
    const convertToCSV = useCallback((data: TimeLine[]): string => {
        const header = "time,result";
        const rows = data.map((item) => `${item.time},${item.result}`);
        return [header, ...rows].join("\n");
    }, []);

    // ランダムな文字列を生成する関数
    const generateRandomString = useCallback((length: number): string => {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        const charactersLength = characters.length;
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }, []);

    // ダウンロード処理
    const handleDownload = useCallback(() => {
        const csvContent = convertToCSV(timeLines);
        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        const randomFileName = `${generateRandomString(16)}.csv`;
        link.href = url;
        link.setAttribute("download", randomFileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }, [convertToCSV, generateRandomString, timeLines]);

    // 指定した動画のパスに動画が存在しているかどうかを確認する
    const handleCheckVideo = useCallback(async () => {
        try {
            const response = await fetch(videoPath);
            if (!response.ok) {
                throw new Error("動画が見つかりませんでした。");
            }
        } catch (error) {
            alert(error);
        }
    }
    , [videoPath]);

    return (
        <Container>
            <Typography
                variant="h5"
                sx={{
                    marginBottom: "4px",
                }}
            >
                メニュー
            </Typography>
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    marginBottom: "16px",
                }}
            >
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "4px",
                    }}
                    onClick={() => {
                        alert("動画を送信しました。");
                    }}
                >
                    動画を送信する
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "4px",
                    }}
                    onClick={() => {
                        alert("解析結果を取得しました。");
                    }}
                >
                    解析結果を取得する
                </Button>
            </Box>
            <Typography
                variant="h5"
                sx={{
                    marginBottom: "4px",
                }}
            >
                解析結果
            </Typography>
            {videoPath && (
                <video
                    src={videoPath}
                    ref={videoRef}
                    controls
                    style={{
                        width: "100%",
                    }}
                />
            )}
            <Box
                sx={{
                    height: "200px",
                    overflowY: "auto",
                    WebkitOverflowScrolling: "touch",
                    scrollbarWidth: "none",
                    boxShadow: "inset 0px 4px 8px rgba(0, 0, 0, 0.3)",
                    padding: "8px",
                    marginBottom: "8px",
                }}
            >
                {timeLines.map((timeLine, index) => (
                    <Typography
                        key={index}
                        component="div"
                        ref={(el) => (timelineRefs.current[index] = el)}
                        sx={{
                            marginBottom: "4px",
                        }}
                    >
                        <b
                            style={{ cursor: "pointer", color: "blue" }}
                            onClick={() => handleTimeClick(timeLine.time)}
                        >
                            {timeLine.time}
                        </b>{" "}
                        {timeLine.result}
                    </Typography>
                ))}
            </Box>
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    marginBottom: "4px",
                }}
            >
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "4px",
                    }}
                    onClick={handleDownload}
                >
                    解析結果をCSVファイルでダウンロード
                </Button>
            </Box>
        </Container>
    );
}
