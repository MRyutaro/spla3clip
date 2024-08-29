import { Box } from "@mui/material";


export default function Header(): JSX.Element {
    return (
        <>
            <Box
                sx={{
                    bgcolor: "secondary.main",
                    color: "white",
                    padding: 1,
                    // textAlign: "center"
                }}
            >
                <h1>
                    スプラ3-キルクリップメーカー
                </h1>
            </Box>
        </>
    );
}
