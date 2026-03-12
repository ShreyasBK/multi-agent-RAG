import { NextRequest, NextResponse } from "next/server";
import { backendClient } from "@/lib/api/client";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const authHeader = req.headers.get("authorization") ?? "";

  const data = await backendClient.chat(body.sessionId, body.query, authHeader);
  return NextResponse.json(data);
}
