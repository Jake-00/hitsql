import axios, { type AxiosRequestConfig } from 'axios'

axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8'

const axiosInstance = axios.create({
  timeout: 10000,
})

axiosInstance.interceptors.request.use(
    (config: any) => {
    return config
  },
  (error: any)  => {
    return Promise.reject(error)
  },
)

axiosInstance.interceptors.response.use(
  (response: any) => {
    if (response?.status === 200 || response?.status === 201) {
      return Promise.resolve(response.data)
    } else {
      return Promise.reject(response)
    }
  },
  (error: any) => {
    if (error?.message?.includes?.('timeout')) {
      console.log('timeout')
    } else {
      console.log(error)
    }
    Promise.reject(error)
  },
)

const request = <ResponseType = unknown>(
  url: string,
  options?: AxiosRequestConfig<unknown>,
): Promise<ResponseType> => {
  return new Promise((resolve, reject) => {
    axiosInstance({
      url,
      ...options,
    })
      .then((res: any) => {
        resolve(res)
      })
      .catch((err: any) => reject(err))
  })
}
export { axiosInstance, request }