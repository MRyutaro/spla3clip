import { Box, Button, Container, Typography } from "@mui/material";
import { useEffect, useRef, useState, useCallback } from "react";
import axios from "axios";

const backendUrl = "http://localhost:8000";


// 時刻とその時刻における解析結果
interface TimeLine {
    // timeはhh:mm:ss形式の文字列
    time: string;
    result: "kill" | "death" | "start" | "finish";
}


export default function App(): JSX.Element {
    const [timeLines, setTimeLines] = useState<TimeLine[]>([]);
    const videoRef = useRef<HTMLVideoElement>(null);
    const timelineRefs = useRef<(HTMLDivElement | HTMLSpanElement | null)[]>([]);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [videoFileName, setVideoFileName] = useState<string>("");
    const [videoPath, setVideoPath] = useState<string>("");

    // 動画ファイルが選択されたときに呼ばれる処理
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setSelectedFile(event.target.files[0]);
        }
    };

    // 動画をサーバーに送信する処理
    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert("ファイルを選択してください。");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            alert("ファイルを送信しています。しばらくお待ちください。");
            // ファイルを送信。成功すればバックエンドからfile_nameが返ってくる
            const response = await axios.post(`${backendUrl}/upload`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            alert("ファイルの送信に成功しました。");
            const videoFileName = response.data.file_name;
            setVideoFileName(videoFileName);
            setVideoPath(`${backendUrl}/uploads/${videoFileName}`);
        } catch (error) {
            alert("ファイルの送信に失敗しました。");
        }
    };

    // 解析タスクを開始する処理
    const postPredictTask = async () => {
        if (!videoFileName) {
            alert("動画ファイルが選択されていません。");
            return;
        }

        try {
            await axios.post(`${backendUrl}/predict/${videoFileName}`);
        } catch (error) {
            alert("解析タスクの開始に失敗しました。");
        }
    }

    // 解析結果を取得する処理
    const fetchResult = async () => {
        try {
            const response = await axios.get(`${backendUrl}/result`);
            const timeLines: TimeLine[] = response.data.time_lines;
            // もしundefinedが返ってきたら空の配列にする
            setTimeLines(timeLines || []);
        } catch (error) {
            alert("解析結果の取得に失敗しました。");
        }
    }

    // 時刻をクリックしたときに呼ばれる処理
    const handleTimeClick = useCallback(
        (time: string) => {
            if (videoRef.current) {
                const [hours, minutes, seconds] = time.split(":").map(Number);
                const secondsToJump = hours * 3600 + minutes * 60 + seconds;
    
                // 一旦停止してから再生する
                videoRef.current.pause(); // 追加
                videoRef.current.currentTime = secondsToJump;
    
                // currentTimeを変更した後に少し遅延を入れて再生する
                setTimeout(() => {
                    videoRef.current?.play();
                }, 100); // 100msの遅延を入れて再生
            }
        },
        [videoRef]
    );

    // 動画の再生位置を監視して、解析結果の時刻に合わせてスクロールする処理
    useEffect(() => {
        const videoElement = videoRef.current;

        const handleTimeUpdate = () => {
            if (videoElement) {
                const currentTime = videoElement.currentTime;

                const closestIndex = timeLines && timeLines.findIndex((timeLine) => {
                    const [hours, minutes, seconds] = timeLine.time
                        .split(":")
                        .map(Number);
                    const timeInSeconds = hours * 3600 + minutes * 60 + seconds;
                    return timeInSeconds >= currentTime;
                });

                if (closestIndex !== -1 && timelineRefs.current[closestIndex]) {
                    timelineRefs.current[closestIndex]?.scrollIntoView({
                        behavior: "smooth",
                        block: "start",
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
        // timeLinesが空の場合はダウンロードしない
        if (timeLines.length === 0) {
            alert("解析結果がありません。");
            return;
        }
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

    return (
        <Container
            sx={{
                WebkitOverflowScrolling: "touch",
                scrollbarWidth: "none",
            }}
        >
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
                <p>
                    1. 動画ファイルを選択する &rarr;{" "}
                    <input type="file" accept="video/*" onChange={handleFileChange} style={{ marginBottom: "8px" }} />
                </p>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleFileUpload}
                    sx={{
                        marginBottom: "8px",
                    }}
                >
                    2. 動画ファイルを送信する
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "8px",
                    }}
                    onClick={postPredictTask}
                >
                    3. 解析を開始する
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    sx={{
                        marginBottom: "8px",
                    }}
                    onClick={fetchResult}
                >
                    4. 解析結果を取得する
                </Button>
            </Box>
            <hr />
            <Typography
                variant="h5"
                sx={{
                    marginBottom: "8px",
                }}
            >
                解析結果
            </Typography>
            {/* videoPathがnullでない場合、動画を表示 */}
            {videoPath && (
                <video
                    src={videoPath}
                    ref={videoRef}
                    controls
                    style={{
                        width: "100%",
                        marginBottom: "8px",
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
                {timeLines.length > 0 ? (
                    timeLines.map((timeLine, index) => (
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
                    ))
                ) : (
                    <Typography>解析結果がありません。</Typography>
                )}
            </Box>
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
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
                    5. 解析結果をCSVファイルでダウンロードする
                </Button>
            </Box>
        </Container>
    );
}
