import { Box, Button, Container, LinearProgress, Typography } from "@mui/material";
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
    const [progress, setProgress] = useState<number>(0);
    const [videoFileName, setVideoFileName] = useState<string | null>(null);
    const [videoPath, setVideoPath] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState<boolean>(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState<boolean>(false);
    const videoRef = useRef<HTMLVideoElement>(null);

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
            setIsUploading(true); // アップロード開始

            // ファイルを送信。成功すればバックエンドからfile_nameが返ってくる
            const response = await axios.post(`${backendUrl}/upload`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            const videoFileName = response.data.file_name;
            setVideoFileName(videoFileName);
            setVideoPath(`${backendUrl}/uploads/${videoFileName}`);
        } catch (error) {
            alert("ファイルの送信に失敗しました。");
        } finally {
            setIsUploading(false); // アップロード完了
        }
    };

    // 解析タスクを開始する処理
    const postPredictTask = async () => {
        if (!videoFileName) {
            alert("動画ファイルが選択されていません。");
            return;
        }

        try {
            setIsProcessing(true);
            await axios.post(`${backendUrl}/predict/${videoFileName}`);
        } catch (error) {
            alert("解析タスクの開始に失敗しました。");
        }
    };

    // 進捗状況をリアルタイムで取得する処理
    useEffect(() => {
        if (!isProcessing) {
            return;
        }

        const eventSource = new EventSource(`${backendUrl}/events`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.progress !== undefined) {
                setProgress(data.progress);
            }
            // 必要に応じて解析結果も更新
            if (data.results) {
                setIsProcessing(false);
                setTimeLines(data.results);
            }
        };

        return () => {
            eventSource.close();
        };
    }, [isProcessing]);

    // 時刻をクリックしたときに呼ばれる処理
    const handleTimeClick = useCallback(
        (time: string) => {
            if (videoRef.current) {
                const [hours, minutes, seconds] = time.split(":").map(Number);
                const secondsToJump = hours * 3600 + minutes * 60 + seconds;
                videoRef.current.currentTime = secondsToJump;
            }
        },
        [videoRef]
    );

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
                {/* アップロード中の場合はプログレスバーを表示 */}
                {isUploading && (
                    <Box sx={{ width: "100%", marginBottom: "16px" }}>
                        <LinearProgress />
                    </Box>
                )}
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
                {/* 進捗状況を表示するためのコンポーネント */}
                <LinearProgress variant="determinate" value={progress} sx={{ marginBottom: "8px" }} />
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
                    4. 解析結果をCSVファイルでダウンロードする
                </Button>
            </Box>
        </Container>
    );
}
