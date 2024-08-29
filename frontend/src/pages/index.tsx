import { Box, Button, Container, LinearProgress, Typography } from "@mui/material";
import { useEffect, useRef, useState, useCallback } from "react";
import axios from "axios";

import Header from "../components/header";
import Footer from "../components/footer";


const backendUrl = "http://localhost:8000";

interface TimeLine {
    time: string;
    result: "kill" | "death" | "start" | "finish";
}

// カスタムボタン
function CustomButton(props: any) {
    // ボタンのスタイルを設定
    return (
        <Button
            variant="contained"
            sx={{
                backgroundColor: "#f4ee28",
                marginBottom: "8px",
                color: "black",
                // カーソルがボタンに乗った時のスタイルを設定
                "&:hover": {
                    backgroundColor: "#d3cd17",
                },
            }}
            {...props}
        >
            {props.children}
        </Button>
    );
}


export default function Index(): JSX.Element {
    const [timeLines, setTimeLines] = useState<TimeLine[]>([]);
    const [progress, setProgress] = useState<number>(0);
    const [videoFileName, setVideoFileName] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState<boolean>(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState<boolean>(false);
    const timelineRefs = useRef<(HTMLDivElement | HTMLSpanElement | null)[]>([]);
    const videoRef = useRef<HTMLVideoElement>(null);
    const [videoObjectUrl, setVideoObjectUrl] = useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            const file = event.target.files[0];
            setSelectedFile(file);

            // ファイルのプレビューURLを設定
            setVideoObjectUrl(URL.createObjectURL(file));
        }
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert("ファイルを選択してください。");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            setIsUploading(true);
            const response = await axios.post(`${backendUrl}/upload`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            const videoFileName = response.data.file_name;
            setVideoFileName(videoFileName);
        } catch (error) {
            alert("ファイルの送信に失敗しました。");
        } finally {
            setIsUploading(false);
        }
    };

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
            if (data.results) {
                setIsProcessing(false);
                setTimeLines(data.results);
            }
        };

        return () => {
            eventSource.close();
        };
    }, [isProcessing]);

    useEffect(() => {
        // コンポーネントのアンマウント時にオブジェクトURLを解放
        return () => {
            if (videoObjectUrl) {
                URL.revokeObjectURL(videoObjectUrl);
            }
        };
    }, [videoObjectUrl]);

    const handleTimeClick = useCallback(
        (time: string) => {
            if (videoRef.current) {
                const [hours, minutes, seconds] = time.split(":").map(Number);
                const secondsToJump = hours * 3600 + minutes * 60 + seconds;
                console.log(videoRef.current.currentTime);
                videoRef.current.currentTime = secondsToJump;
                videoRef.current.play();
                console.log(videoRef.current.currentTime);
            }
        },
        [videoRef]
    );

    const convertToCSV = useCallback((data: TimeLine[]): string => {
        const header = "time,result";
        const rows = data.map((item) => `${item.time},${item.result}`);
        return [header, ...rows].join("\n");
    }, []);

    const generateRandomString = useCallback((length: number): string => {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        const charactersLength = characters.length;
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }, []);

    const handleDownload = useCallback(() => {
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
        <>
            <Header />
            <Container
                sx={{
                    WebkitOverflowScrolling: "touch",
                    scrollbarWidth: "none",
                    marginY: "32px",
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
                    <CustomButton onClick={handleFileUpload}>2. 動画ファイルをアップロードする</CustomButton>
                    {/* もしアップロード中ならプログレスバーを表示、そうでなければ0%のプログレスバーを表示、アップロードが完了したら100%のプログレスバーを表示 */}
                    {isUploading ? (
                        <LinearProgress variant="indeterminate" sx={{ marginBottom: "8px" }} />
                    ) : (
                        <LinearProgress variant="determinate" value={videoFileName ? 100 : 0} sx={{ marginBottom: "8px" }} />
                    )}
                    <CustomButton onClick={postPredictTask}>3. 解析を開始する</CustomButton>
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
                {videoObjectUrl && (
                    <video
                        src={videoObjectUrl}
                        ref={videoRef}
                        controls
                        muted
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
                    {timeLines.length > 0 ? (
                        timeLines.map((timeLine, index) => (
                            <Typography
                                key={index}
                                sx={{
                                    marginBottom: "4px",
                                }}
                            >
                                <b
                                    key={index}
                                    ref={(el) => {
                                        timelineRefs.current[index] = el;
                                    }}
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
                    <CustomButton onClick={handleDownload}>4. 解析結果をCSVファイルでダウンロードする</CustomButton>
                </Box>
            </Container>
            <Footer />
        </>
    );
}
