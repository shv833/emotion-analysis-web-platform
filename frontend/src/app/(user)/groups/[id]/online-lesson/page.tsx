'use client'
import { useEffect, useRef } from 'react'
import { AuthActions } from '@/app/(auth)/utils'

const { getToken } = AuthActions()
const token = getToken('access')

type Props = {
  params: { id: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

const OnlineLessonPage = ({ params }: Props) => {
  const id = params.id
  const localVideoRef = useRef<HTMLVideoElement>(null)
  const remoteVideoRef = useRef<HTMLVideoElement>(null)
  const peerConnection = useRef<RTCPeerConnection | null>(null)
  const webSocket = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (id && token) {
      webSocket.current = new WebSocket(
        `ws://localhost/ws/videocall/${id}/?token=${token}`
      )

      webSocket.current.onopen = () => {
        console.log('WebSocket connection opened')
        setupWebRTC()
      }

      webSocket.current.onmessage = (event) => {
        const data = JSON.parse(event.data)
        handleSignalingData(data)
      }

      webSocket.current.onclose = () => {
        console.log('WebSocket connection closed')
      }
    }

    return () => {
      if (webSocket.current) {
        webSocket.current.close()
      }
      if (peerConnection.current) {
        peerConnection.current.close()
      }
    }
  }, [id])

  const setupWebRTC = async () => {
    try {
      const localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      })
      if (localVideoRef.current) {
        localVideoRef.current.srcObject = localStream
      }

      const configuration = {
        iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
      }

      peerConnection.current = new RTCPeerConnection(configuration)
      localStream.getTracks().forEach((track) => {
        if (peerConnection.current) {
          peerConnection.current.addTrack(track, localStream)
        }
      })

      peerConnection.current.ontrack = (event) => {
        if (remoteVideoRef.current) {
          remoteVideoRef.current.srcObject = event.streams[0]
        }
      }

      peerConnection.current.onicecandidate = (event) => {
        if (event.candidate && webSocket.current) {
          webSocket.current.send(
            JSON.stringify({
              type: 'ice-candidate',
              candidate: event.candidate,
            })
          )
        }
      }

      const offer = await peerConnection.current.createOffer()
      await peerConnection.current.setLocalDescription(offer)
      if (webSocket.current) {
        webSocket.current.send(JSON.stringify({ type: 'offer', offer }))
      }
    } catch (error) {
      console.error('Error accessing media devices.', error)
    }
  }

  const handleSignalingData = async (data: any) => {
    switch (data.type) {
      case 'offer':
        if (peerConnection.current) {
          await peerConnection.current.setRemoteDescription(
            new RTCSessionDescription(data.offer)
          )
          const answer = await peerConnection.current.createAnswer()
          await peerConnection.current.setLocalDescription(answer)
          if (webSocket.current) {
            webSocket.current.send(JSON.stringify({ type: 'answer', answer }))
          }
        }
        break
      case 'answer':
        if (peerConnection.current) {
          await peerConnection.current.setRemoteDescription(
            new RTCSessionDescription(data.answer)
          )
        }
        break
      case 'ice-candidate':
        if (peerConnection.current) {
          await peerConnection.current.addIceCandidate(
            new RTCIceCandidate(data.candidate)
          )
        }
        break
      default:
        break
    }
  }

  return (
    <div>
      <h1>Online Lesson for Group {id}</h1>
      <div>
        <video ref={localVideoRef} autoPlay playsInline muted></video>
        <video ref={remoteVideoRef} autoPlay playsInline></video>
      </div>
    </div>
  )
}

export default OnlineLessonPage
