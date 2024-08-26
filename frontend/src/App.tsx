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

function App(): JSX.Element {
    const [timeLines, setTimeLines] = useState<TimeLine[]>([]);
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        setTimeLines(initialTimeLines);
    }, []);

    const handleTimeClick = useCallback((time: string) => {
        if (videoRef.current) {
            const [hours, minutes, seconds] = time.split(":").map(Number);
            const secondsToJump = hours * 3600 + minutes * 60 + seconds;
            videoRef.current.currentTime = secondsToJump;
            videoRef.current.play();
        }
    }, [videoRef]);

    return (
        <Container>
            <video
                ref={videoRef}
                src="/background.mp4"
                controls
                style={{
                    width: "100%",
                }}
            />
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
                    marginBottom: "4px",
                }}
            >
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "4px",
                    }}
                    onClick={() => { alert("動画を送信しました。") }}
                >
                    動画を送信する
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "4px",
                    }}
                    onClick={() => { alert("解析結果を取得しました。") }}
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
            <Box>
                {timeLines.map((timeLine, index) => (
                    <Typography
                        key={index}
                        sx={{
                            marginBottom: "4px",
                        }}
                    >
                        <b
                            style={{ cursor: "pointer", color: "blue" }}
                            onClick={() => handleTimeClick(timeLine.time)}
                        >
                            {timeLine.time}
                        </b> {timeLine.result}
                    </Typography>
                ))}
            </Box>
        </Container>
    );
}

export default App;
